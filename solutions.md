Solution 1: 

flowchart TD
    X["user"] --> Z["Portal - upload docs"]
    Z --> A["Backend Storage"]
    A --> B{"Bank Statement Agent"} & C{"Credit Report Agent"}
    B --> Y["Bank Statement Service"]
    C --> T["Credit Report Service"]
    B -- Verification Data --> D{"Coordinator Agent"}
    C -- Verification Data --> D
    D --> R{"Supervisor Agent"}
    R -- Determines Next Steps --> E["Output: Approved, Flagged for Review, etc."]
    T --> n1["External Vendors"]

    X@{ icon: "fa:circle-user", pos: "b"}
    style A stroke:#00C853
    style B stroke:#2962FF
    style C stroke:#2962FF
    style D stroke:#2962FF
    style R stroke:#2962FF

---------

Solution 2: 

graph TD
    A[Data Ingestion: Bank Statement & Credit Report] --> B{Bank Statement Agent};
    A --> C{Credit Report Agent};
    B -- Extracted Data --> D[Data Hub];
    C -- Extracted Data --> D;
    D -- Data Available --> E{Coordinator Agent};
    E -- Compares Data --> F{Supervisor Agent};
    F -- Determines Next Steps --> G[Output: Approved, Flagged for Review, etc.];


--------
Solution 3 

graph TD
    A[Data Ingestion] --> B[Message Broker];
    B -- Document Ready Event --> C{Bank Statement Agent};
    B -- Document Ready Event --> D{Credit Report Agent};
    C -- Extracted Data Event --> B;
    D -- Extracted Data Event --> B;
    B -- Extracted Data Events --> E{Verification Agent};
    E -- Verification Result Event --> B;
    B -- Verification Result Event --> F{Supervisor Agent};
    F -- Determines Next Steps --> G[Output: Approved, Flagged for Review, etc.];

    