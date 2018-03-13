# sales_proc
A data processing utility application

## Basic Architecture

- API Initialize (on-demand or cron based)
	- Required parameters
		- basic security (origin or token? Don't know. )
		- raw data (or data location)
	- Optional parameters
		- Instruction to return raw or formatted data.
		- Instruction to send data to third party.
- get data (database or accept with call)
- process into 
- return data