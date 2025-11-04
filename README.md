# agentic_usecase_1

## Use case
Build an agentic solution for document verification  Bank statements and credit reports are critical documetns for our operation. the goal is to create an agentic setup where an agent reviewing a credit report consults with an agent reviewing a bank statemetn to verify customer name and address. the supervisor agent then determine the next steps based on the verification data.

## Solution 

An agentic solution for document verification, particularly for critical documents like bank statements and credit reports, can significantly streamline operations and enhance accuracy.  
Here are 3 potential solutions - with C4 model. 

### Solution 1: Sequential Agent Collaboration
This model follows a clear, top-down structure where specialized agents handle individual document analysis and report to a supervising agent for a final decision.


### Solution 2: Centralized Data Hub with a Coordinator Agent
In this approach, a central repository holds the extracted information, and a coordinator agent orchestrates the verification process, allowing for more parallel processing.


### Solution 3: Event-Driven Architecture with an Event Bus 
This sophisticated model uses a message broker to decouple the agents, allowing for a highly scalable and resilient system.

## Trade Off


| Factors  | Sequenctial | Central Data   | Event Driven|
|-------|-----|-------|-------|
 | Complexity | Low - linear solution | Medium - data pipeline and orchestration | High - distributed and asyn nature makes the system complex to design and debug. | 
 |Scalability | Moderate | Good | High|
 | Latency | high - sequential| low  - parallel processing | low - realtime, asyn processing and high throughput |
 |Resiliency | Low - chain will hault | moderate - coordinator plays a single point of failure| High - decoupled system|
 |Maintainance| low | moderate | high|
 |Flexibility | low| moderate| high| 
 | Best | low traffic, implementation speed | moderate volume, central layer for audit (Source of truth) | High volume complex and cirtical usecase| 
 

## Proof of Concept


