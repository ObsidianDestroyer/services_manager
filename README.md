# Services manager application
- - -
This application is built for manage services on your server. \
You are can run this application with command: `sudo python .` \
Includes simple REST API:
##### [GET] method:
> Bare **GET** request:  `$HOST/api/services`
##### Response "200 OK":
```json
[
  {
    "serviceID": 1,
    "serviceName": "vsftpd",
    "serviceStatus": false,
    "serviceLock": false
  },
  {
    "serviceID": 2,
    "serviceName": "sshd",
    "serviceStatus": false,
    "serviceLock": false
  }
]
```
`serviceID` is internal identity of service in SQLite database. \
`serviceName` is a unique name specified for the service and equal to the name of the real system service. \
`serviceStatus` the label of the current status of the service; `true` - works; `false` - service stopped. \
`ServiceLock` the label of the current lock state of the service; `true` - stopped due an error; `false` - not locked, available to use. If the service lock status is `true`, then the service cannot be started.
- - -
##### [POST] method:
> **POST** request with query params:  `$HOST/api/services?serviceName=vsftpd&action=start`
To interact with the service you need to specify the values of the keys "serviceName" and "action".
Available **serviceName**'s can be obtained from the **GET** request described above.
Available **action**'s is:
- **start**
- **stop**
- **restart**
##### Response "200 OK":
```json
{
  "serviceID": 1,
  "serviceName": "vsftpd",
  "serviceStatus": true,
  "serviceLock": false
}
```
### Error responses:
Includes key **error** with description of occurred error.
##### 500 Internal Server Error:
```json
{
  "serviceID": 1,
  "serviceName": "vsftpd",
  "serviceStatus": false,
  "serviceLock": false,
  "error": "failed to stop/restart service due an error"
}
```
##### 303 See Other:
```json
{
  "serviceID": 1,
  "serviceName": "vsftpd",
  "serviceStatus": false,
  "serviceLock": false,
  "error": "application already running"
}
```
##### 400 Bad Request:
```json
{
  "error": "bad query params"
}
```
##### 400 Bad Request:
```json
{
  "error": "bad action 'reload'"
}
```
