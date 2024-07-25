/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This software may be used and distributed according to the terms of the
 * GNU General Public License version 2.
 */

use anyhow::Context;
use anyhow::Result;
use async_trait::async_trait;
use context::CoreContext;
use metaconfig_types::HookConfig;
use mononoke_types::BasicFileChange;
use mononoke_types::FileType;
use mononoke_types::NonRootMPath;
use serde::Deserialize;

use crate::CrossRepoPushSource;
use crate::FileHook;
use crate::HookExecution;
use crate::HookFileContentProvider;
use crate::HookRejectionInfo;
use crate::PushAuthoredBy;

#[derive(Debug, Deserialize, Clone)]
pub struct NoExecutableBinariesConfig {
    /// Message to include in the hook rejection if an executable binary file is
    /// is committed.
    /// ${filename} => The path of the file along with the filename
    illegal_executable_binary_message: String,
}

/// Hook to block commits containing files with illegal name patterns
#[derive(Clone, Debug)]
pub struct NoExecutableBinariesHook {
    config: NoExecutableBinariesConfig,
}

impl NoExecutableBinariesHook {
    pub fn new(config: &HookConfig) -> Result<Self> {
        let config = config
            .parse_options()
            .context("Missing or invalid JSON hook configuration for no-executable-files hook")?;
        Ok(Self::with_config(config))
    }

    pub fn with_config(config: NoExecutableBinariesConfig) -> Self {
        Self { config }
    }
}

#[async_trait]
impl FileHook for NoExecutableBinariesHook {
    async fn run<'this: 'change, 'ctx: 'this, 'change, 'fetcher: 'change, 'path: 'change>(
        &'this self,
        ctx: &'ctx CoreContext,
        content_manager: &'fetcher dyn HookFileContentProvider,
        change: Option<&'change BasicFileChange>,
        path: &'path NonRootMPath,
        _cross_repo_push_source: CrossRepoPushSource,
        _push_authored_by: PushAuthoredBy,
    ) -> Result<HookExecution> {
        let content_id = match change {
            Some(basic_fc) => {
                if basic_fc.file_type() != FileType::Executable {
                    // Not an executable, so passes hook right away
                    return Ok(HookExecution::Accepted);
                };
                basic_fc.content_id()
            }
            _ => {
                // File change is not committed, so passes hook
                return Ok(HookExecution::Accepted);
            }
        };
        let content_metadata = content_manager.get_file_metadata(ctx, content_id).await?;

        if content_metadata.is_binary {
            return Ok(HookExecution::Rejected(HookRejectionInfo::new_long(
                "Illegal executable file",
                self.config
                    .illegal_executable_binary_message
                    .replace("${filename}", &path.to_string()),
            )));
        } else {
            Ok(HookExecution::Accepted)
        }
    }
}

#[cfg(test)]
mod test {

    use std::collections::HashMap;
    use std::collections::HashSet;

    use anyhow::anyhow;
    use blobstore::Loadable;
    use borrowed::borrowed;
    use fbinit::FacebookInit;
    use maplit::hashmap;
    use maplit::hashset;
    use mononoke_types::BonsaiChangeset;
    use repo_hook_file_content_provider::RepoHookFileContentProvider;
    use tests_utils::BasicTestRepo;
    use tests_utils::CreateCommitContext;

    use super::*;

    /// Create default test config that each test can customize.
    fn make_test_config() -> NoExecutableBinariesConfig {
        NoExecutableBinariesConfig {
            illegal_executable_binary_message: "Executable file '${filename}' can't be committed."
                .to_string(),
        }
    }

    async fn test_setup(
        fb: FacebookInit,
    ) -> (
        CoreContext,
        BasicTestRepo,
        RepoHookFileContentProvider,
        NoExecutableBinariesHook,
    ) {
        let ctx = CoreContext::test_mock(fb);
        let repo: BasicTestRepo = test_repo_factory::build_empty(ctx.fb)
            .await
            .expect("Failed to create test repo");
        let content_manager = RepoHookFileContentProvider::new(&repo);
        let config = make_test_config();
        let hook = NoExecutableBinariesHook::with_config(config);

        (ctx, repo, content_manager, hook)
    }

    async fn assert_hook_execution(
        ctx: &CoreContext,
        content_manager: RepoHookFileContentProvider,
        bcs: BonsaiChangeset,
        hook: NoExecutableBinariesHook,
        valid_files: HashSet<&str>,
        illegal_files: HashMap<&str, &str>,
    ) -> Result<()> {
        for (path, change) in bcs.file_changes() {
            let hook_execution = hook
                .run(
                    ctx,
                    &content_manager,
                    change.simplify(),
                    path,
                    CrossRepoPushSource::NativeToThisRepo,
                    PushAuthoredBy::User,
                )
                .await?;

            match hook_execution {
                HookExecution::Accepted => assert!(valid_files.contains(path.to_string().as_str())),
                HookExecution::Rejected(info) => {
                    let expected_info_msg = illegal_files
                        .get(path.to_string().as_str())
                        .ok_or(anyhow!("Unexpected rejected file"))?;
                    assert_eq!(info.long_description, expected_info_msg.to_string())
                }
            }
        }

        Ok(())
    }

    /// Test that the hook rejects an executable binary file
    #[fbinit::test]
    async fn test_reject_single_executable_binary(fb: FacebookInit) -> Result<()> {
        let (ctx, repo, content_manager, hook) = test_setup(fb).await;

        borrowed!(ctx, repo);

        let cs_id = CreateCommitContext::new_root(ctx, repo)
            .add_file_with_type(
                "foo/bar/exec",
                vec![b'\0', 0x4D, 0x5A],
                FileType::Executable,
            )
            .add_file("bar/baz/hoo.txt", "a")
            .add_file("foo bar/baz", "b")
            .commit()
            .await?;

        let bcs = cs_id.load(ctx, &repo.repo_blobstore).await?;

        let valid_files: HashSet<&str> = hashset! {"foo bar/baz", "bar/baz/hoo.txt" };

        let illegal_files: HashMap<&str, &str> =
            hashmap! {"foo/bar/exec" => "Executable file 'foo/bar/exec' can't be committed."};

        assert_hook_execution(ctx, content_manager, bcs, hook, valid_files, illegal_files).await
    }

    /// Test that the hook rejects multiple executable binaries
    #[fbinit::test]
    async fn test_reject_multiple_executable_binaries(fb: FacebookInit) -> Result<()> {
        let (ctx, repo, content_manager, hook) = test_setup(fb).await;

        borrowed!(ctx, repo);

        let cs_id = CreateCommitContext::new_root(ctx, repo)
            .add_file_with_type(
                "foo/bar/exec",
                vec![b'\0', 0x4D, 0x5A],
                FileType::Executable,
            )
            .add_file_with_type(
                "foo/bar/another_exec",
                vec![0xB0, b'\0', 0x5A],
                FileType::Executable,
            )
            .add_file("bar/baz/hoo.txt", "a")
            .add_file("foo bar/baz", "b")
            .commit()
            .await?;

        let bcs = cs_id.load(ctx, &repo.repo_blobstore).await?;

        let valid_files: HashSet<&str> = hashset! {"foo bar/baz", "bar/baz/hoo.txt" };

        let illegal_files: HashMap<&str, &str> = hashmap! {
            "foo/bar/exec" => "Executable file 'foo/bar/exec' can't be committed.",
            "foo/bar/another_exec" => "Executable file 'foo/bar/another_exec' can't be committed."
        };

        assert_hook_execution(ctx, content_manager, bcs, hook, valid_files, illegal_files).await
    }

    /// That that non-executable binaries pass
    #[fbinit::test]
    async fn test_non_executable_binaries_pass(fb: FacebookInit) -> Result<()> {
        let (ctx, repo, content_manager, hook) = test_setup(fb).await;

        borrowed!(ctx, repo);

        let cs_id = CreateCommitContext::new_root(ctx, repo)
            .add_file("foo/bar/exec", vec![b'\0', 0x4D, 0x5A])
            .add_file("bar/baz/hoo.txt", "a")
            .add_file("foo bar/baz", "b")
            .commit()
            .await?;

        let bcs = cs_id.load(ctx, &repo.repo_blobstore).await?;

        let valid_files: HashSet<&str> =
            hashset! {"foo/bar/exec", "foo bar/baz", "bar/baz/hoo.txt" };

        let illegal_files: HashMap<&str, &str> = hashmap! {};

        assert_hook_execution(ctx, content_manager, bcs, hook, valid_files, illegal_files).await
    }

    /// That that executable scripts pass
    #[fbinit::test]
    async fn test_executable_scripts_pass(fb: FacebookInit) -> Result<()> {
        let (ctx, repo, content_manager, hook) = test_setup(fb).await;

        borrowed!(ctx, repo);

        let cs_id = CreateCommitContext::new_root(ctx, repo)
            .add_file("foo/bar/baz", "a")
            .add_file("foo bar/quux", "b")
            .add_file_with_type("bar/baz/hoo.txt", "c", FileType::Executable)
            .commit()
            .await?;

        let bcs = cs_id.load(ctx, &repo.repo_blobstore).await?;

        let valid_files: HashSet<&str> =
            hashset! {"foo/bar/baz", "foo bar/quux", "bar/baz/hoo.txt" };

        let illegal_files: HashMap<&str, &str> = hashmap! {};

        assert_hook_execution(ctx, content_manager, bcs, hook, valid_files, illegal_files).await
    }

    /// That that changes without executable file types are still allowed
    #[fbinit::test]
    async fn test_changes_without_binaries_pass(fb: FacebookInit) -> Result<()> {
        let (ctx, repo, content_manager, hook) = test_setup(fb).await;

        borrowed!(ctx, repo);

        let cs_id = CreateCommitContext::new_root(ctx, repo)
            .add_file("foo/bar/baz", "a")
            .add_file("foo bar/quux", "b")
            .add_file("bar/baz/hoo.txt", "c")
            .commit()
            .await?;

        let bcs = cs_id.load(ctx, &repo.repo_blobstore).await?;

        let valid_files: HashSet<&str> =
            hashset! {"foo/bar/baz", "foo bar/quux", "bar/baz/hoo.txt" };

        let illegal_files: HashMap<&str, &str> = hashmap! {};

        assert_hook_execution(ctx, content_manager, bcs, hook, valid_files, illegal_files).await
    }
}
