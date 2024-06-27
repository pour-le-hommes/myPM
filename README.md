# OVerall Architecture

graph TD
    classDef backend fill:#ADD8E6;
    classDef api fill:#90EE90;
    classDef cache fill:#E6E6FA;
    classDef database fill:#FFFFE0;

    subgraph Backend
        direction TB
        Server[Server]
        TaskProcessor[Task Processor]
        APIGateway[API Gateway]
        FinancialDataCache[Financial Data Cache]
        class Server,TaskProcessor,APIGateway,FinancialDataCache backend
    end

    subgraph API
        direction TB
        DiscordAPI[Discord API]
        GoogleSheetsAPI[Google Sheets API]
        GroqAPI[Groq API]
        class DiscordAPI,GoogleSheetsAPI,GroqAPI api
    end

    subgraph Database
        direction TB
        Supabase[Supabase]
        class Supabase database
    end

    DiscordBot[Discord Bot] -->|Connect to Cache| FinancialDataCache
    DiscordBot -->|General Commands| Server

    Server -->|API Request| APIGateway
    Server -->|Data Processing Request| TaskProcessor
    Server -->|Check/Update Cache| FinancialDataCache

    APIGateway -->|Communicate with Discord| DiscordAPI
    APIGateway -->|Communicate| GroqAPI
    APIGateway -->|Retrieve Financial Data (if not cached)| GoogleSheetsAPI

    TaskProcessor -->|Query/Update Data| Supabase
    TaskProcessor -->|Processed Data Response| Server
    TaskProcessor -->|Processed Data Response| GroqAPI

    FinancialDataCache -->|Cached Financial Data| Server


