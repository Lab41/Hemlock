### 0.1.4 (2013-09-23)

- finished query-data, including making results specific to users and the systems they have access to via the tenants they and the systems belong to
- finished scheduler
- more progress on breaking out hfs, moving previous working hfs to hfs_old (untested)
- added ability to make the scheduler distributed
- added schedule-server api calls
- bug fixes

### 0.1.3 (2013-09-16)

- stubbed breaking out hfs into a more modular structure (incomplete)
- added man page and lots more documentation
- added query-data to API (incomplete)
- added version to argument options
- added lots of debugging and capability to get debugging statements using -D
- bug fixes

### 0.1.2 (2013-09-03)

- added storing of client and hemlock creds in mysql
- greatly improved client and schedule api calls
- improved streaming client support
- moved majority of hemlock function calls to be done directly through hemlock, rather than other classes
- bug fixes

### 0.1.1 (2013-08-23)

- small additions to the api for clients and schedules
- bug fixes
- improved MySQL client support related to memory issues

### 0.1.0 (2013-08-12)

- basic proof-of-concept
- supports a handful of clients including MySQL, Redis, MongoDB, and Local FileSystems
- experimental support for streams
- basic security model around users, tenants, systems, and roles
- robust CLI for managing users, tenants, systems, and roles
