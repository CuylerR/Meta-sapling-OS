/*
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This software may be used and distributed according to the terms of the
 * GNU General Public License version 2.
 */

#pragma once

#ifndef _WIN32

// https://datatracker.ietf.org/doc/rfc5531/?include_text=1

#include <vector>

#include <folly/Preprocessor.h>
#include "eden/fs/nfs/xdr/Xdr.h"

// This is a macro that is used to emit the implementation of XDR serialization,
// deserialization and operator== for a type.
//
// The parameters the type name followed by the list of field names.
// The field names must be listed in the same order as the RPC/XDR
// definition for the type requires.  It is good practice to have that
// order match the order of the fields in the struct.
//
// Example: in the header file:
//
// struct Foo {
//    int bar;
//    int baz;
// };
// EDEN_XDR_SERDE_DECL(Foo);
//
// Then in the cpp file:
//
// EDEN_XDR_SERDE_IMPL(Foo, bar, baz);

// This macro declares the XDR serializer and deserializer functions
// for a given type.
// See EDEN_XDR_SERDE_IMPL above for an example.
#define EDEN_XDR_SERDE_DECL(STRUCT, ...)                   \
  bool operator==(const STRUCT& a, const STRUCT& b);       \
  template <>                                              \
  struct XdrTrait<STRUCT> {                                \
    static void serialize(                                 \
        folly::io::QueueAppender& appender,                \
        const STRUCT& a) {                                 \
      FOLLY_PP_FOR_EACH(EDEN_XDR_SER, __VA_ARGS__)         \
    }                                                      \
    static STRUCT deserialize(folly::io::Cursor& cursor) { \
      STRUCT ret;                                          \
      FOLLY_PP_FOR_EACH(EDEN_XDR_DE, __VA_ARGS__)          \
      return ret;                                          \
    }                                                      \
  }

#define EDEN_XDR_SERDE_IMPL(STRUCT, ...)                  \
  bool operator==(const STRUCT& a, const STRUCT& b) {     \
    return FOLLY_PP_FOR_EACH(EDEN_XDR_EQ, __VA_ARGS__) 1; \
  }

// Implementation details for the macros above:

// This is a helper called by FOLLY_PP_FOR_EACH. It emits a call to
// the serializer for a given field name
#define EDEN_XDR_SER(name) \
  XdrTrait<decltype(a.name)>::serialize(appender, a.name);

// This is a helper called by FOLLY_PP_FOR_EACH. It emits a call to
// the de-serializer for a given field name.
#define EDEN_XDR_DE(name) \
  ret.name = XdrTrait<decltype(ret.name)>::deserialize(cursor);

// This is a helper called by FOLLY_PP_FOR_EACH. It emits a comparison
// between a.name and b.name, followed by &&.  It is intended
// to be used in a sequence and have a literal 1 following that sequence.
// It is used to generator the == operator for a type.
// It is present primarily for testing purposes.
#define EDEN_XDR_EQ(name) a.name == b.name&&

namespace facebook::eden {

enum class auth_flavor {
  AUTH_NONE = 0,
  AUTH_SYS = 1,
  AUTH_UNIX = 1, /* AUTH_UNIX is the same as AUTH_SYS */
  AUTH_SHORT = 2,
  AUTH_DH = 3,
  RPCSEC_GSS = 6
  /* and more to be defined */
};

enum class msg_type {
  CALL = 0,
  REPLY = 1,
};

enum class reply_stat { MSG_ACCEPTED = 0, MSG_DENIED = 1 };

enum class accept_stat {
  SUCCESS = 0, /* RPC executed successfully       */
  PROG_UNAVAIL = 1, /* remote hasn't exported program  */
  PROG_MISMATCH = 2, /* remote can't support version #  */
  PROC_UNAVAIL = 3, /* program can't support procedure */
  GARBAGE_ARGS = 4, /* procedure can't decode params   */
  SYSTEM_ERR = 5 /* e.g. memory allocation failure  */
};

enum class reject_stat {
  RPC_MISMATCH = 0, /* RPC version number != 2          */
  AUTH_ERROR = 1 /* remote can't authenticate caller */
};

enum class auth_stat {
  AUTH_OK = 0, /* success                        */
  /*
   * failed at remote end
   */
  AUTH_BADCRED = 1, /* bad credential (seal broken)   */
  AUTH_REJECTEDCRED = 2, /* client must begin new session  */
  AUTH_BADVERF = 3, /* bad verifier (seal broken)     */
  AUTH_REJECTEDVERF = 4, /* verifier expired or replayed   */
  AUTH_TOOWEAK = 5, /* rejected for security reasons  */
  /*
   * failed locally
   */
  AUTH_INVALIDRESP = 6, /* bogus response verifier        */
  AUTH_FAILED = 7, /* reason unknown                 */
  /*
   * AUTH_KERB errors; deprecated.  See [RFC2695]
   */
  AUTH_KERB_GENERIC = 8, /* kerberos generic error */
  AUTH_TIMEEXPIRE = 9, /* time of credential expired */
  AUTH_TKT_FILE = 10, /* problem with ticket file */
  AUTH_DECODE = 11, /* can't decode authenticator */
  AUTH_NET_ADDR = 12, /* wrong net address in ticket */
  /*
   * RPCSEC_GSS GSS related errors
   */
  RPCSEC_GSS_CREDPROBLEM = 13, /* no credentials for user */
  RPCSEC_GSS_CTXPROBLEM = 14 /* problem with context */
};

using OpaqueBytes = std::vector<uint8_t>;

struct opaque_auth {
  auth_flavor flavor;
  OpaqueBytes body;
};
EDEN_XDR_SERDE_DECL(opaque_auth, flavor, body);

constexpr uint32_t kRPCVersion = 2;

struct call_body {
  uint32_t rpcvers; /* must be equal to kRPCVersion */
  uint32_t prog;
  uint32_t vers;
  uint32_t proc;
  opaque_auth cred;
  opaque_auth verf;
  /* procedure-specific parameters start here */
};
EDEN_XDR_SERDE_DECL(call_body, rpcvers, prog, vers, proc, cred, verf);

struct rpc_msg_call {
  uint32_t xid;
  msg_type mtype; // msg_type::CALL
  call_body cbody;
};
EDEN_XDR_SERDE_DECL(rpc_msg_call, xid, mtype, cbody);

struct mismatch_info {
  uint32_t low;
  uint32_t high;
};
EDEN_XDR_SERDE_DECL(mismatch_info, low, high);

struct accepted_reply {
  opaque_auth verf;
  accept_stat stat;
};
EDEN_XDR_SERDE_DECL(accepted_reply, verf, stat);

struct rejected_reply
    : public XdrVariant<reject_stat, mismatch_info, auth_stat> {};

template <>
struct XdrTrait<rejected_reply> : public XdrTrait<rejected_reply::Base> {
  static rejected_reply deserialize(folly::io::Cursor& cursor) {
    rejected_reply ret;
    ret.tag = XdrTrait<reject_stat>::deserialize(cursor);
    switch (ret.tag) {
      case reject_stat::RPC_MISMATCH:
        ret.v = XdrTrait<mismatch_info>::deserialize(cursor);
        break;
      case reject_stat::AUTH_ERROR:
        ret.v = XdrTrait<auth_stat>::deserialize(cursor);
        break;
    }
    return ret;
  }
};

struct reply_body
    : public XdrVariant<reply_stat, accepted_reply, rejected_reply> {};

template <>
struct XdrTrait<reply_body> : public XdrTrait<reply_body::Base> {
  static reply_body deserialize(folly::io::Cursor& cursor) {
    reply_body ret;
    ret.tag = XdrTrait<reply_stat>::deserialize(cursor);
    switch (ret.tag) {
      case reply_stat::MSG_ACCEPTED:
        ret.v = XdrTrait<accepted_reply>::deserialize(cursor);
        break;
      case reply_stat::MSG_DENIED:
        ret.v = XdrTrait<rejected_reply>::deserialize(cursor);
        break;
    }
    return ret;
  }
};

struct rpc_msg_reply {
  uint32_t xid;
  msg_type mtype; // msg_type::REPLY
  reply_body rbody;
};
EDEN_XDR_SERDE_DECL(rpc_msg_reply, xid, mtype, rbody);

void serializeReply(
    folly::io::QueueAppender& ser,
    accept_stat status,
    uint32_t xid);

struct authsys_parms {
  uint32_t stamp;
  std::string machinename;
  uint32_t uid;
  uint32_t gid;
  std::vector<uint32_t> gids;
};
EDEN_XDR_SERDE_DECL(authsys_parms, stamp, machinename, uid, gid, gids);

} // namespace facebook::eden

#endif
