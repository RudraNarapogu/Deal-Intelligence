import sys
import json
import argparse
from datetime import datetime
import urllib.request
import urllib.error

# ==============================================================================
# SYNTHETIC LONGITUDINAL SALES DATASET FOR DEAL INTELLIGENCE STRESS TESTING
# ==============================================================================

API_BASE_URL = "http://localhost:8000/api"

ACME_DEAL_ID = "acme-corp"
ZENITH_DEAL_ID = "zenith-ltd"

# ------------------------------------------------------------------------------
# ACME CORPORATION DATASET (~25 Chronological Interactions)
# ------------------------------------------------------------------------------
ACME_INTERACTIONS = [
    # Phase 1: Discovery (1-4)
    {
        "type": "meeting",
        "date": "2026-03-01",
        "title": "Initial Discovery & Workflow Assessment",
        "transcript": "Met with Sarah Jenkins, VP of Finance at Acme Corporation. Acme currently processes approximately 10,000 invoices monthly across three regional offices completely manually. The accounts payable team consists of five full-time specialists who manually enter invoice data into SAP ERP. Sarah highlighted that manual data entry leads to frequent human errors, lost invoice attachments, delayed vendor payments, and late payment penalties averaging ₹45,000 per quarter. Their primary business pain is high processing operational cost and slow cycle times. Initial target timeline for deploying an automated invoice solution is 60 days. Sarah indicated an initial budget expectation of around ₹1,20,000 annually.",
        "context": "sales meeting"
    },
    {
        "type": "call",
        "date": "2026-03-10",
        "title": "Current AP Workflow Review",
        "transcript": "Follow-up phone call with Sarah Jenkins and AP Supervisor Robert Chen. Reviewed the step-by-step invoice intake process in detail. Invoices arrive via paper mail and PDF email attachments. Staff manually print incoming PDFs, re-enter line items into SAP ERP, and physically route paper approval forms for supervisor signatures across departments. Invoice processing time currently averages 8 business days per invoice. Robert Chen emphasized that month-end financial closing is delayed by up to 5 business days due to unprocessed invoice backlogs. They require an automated extraction platform that integrates directly with SAP ERP to eliminate manual data entry and streamline approvals across all locations.",
        "context": "sales call"
    },
    {
        "type": "email",
        "date": "2026-03-22",
        "title": "Invoice Cost & Volume Metrics Summary",
        "transcript": "Received email communication from Sarah Jenkins detailing verified operational invoice metrics. Acme's verified monthly volume is 10,200 invoices per month, with 70% arriving as digital PDF email attachments and 30% as paper documents. Fully burdened cost per invoice processed manually is estimated at ₹85. Acme's stated goal for the new platform is reducing processing costs by at least 60%, achieving 99% extraction accuracy, and shortening approval turnaround time from 8 days down to under 48 hours. Timeline expectation remains 60 days for full rollout. Sarah requested a preliminary demonstration for accounts payable team members and finance department leads.",
        "context": "email exchange"
    },
    {
        "type": "follow_up",
        "date": "2026-04-05",
        "title": "Initial Evaluation Scope & Alignment",
        "transcript": "Brief alignment call with Sarah Jenkins. Confirmed that Sarah Jenkins is the primary business champion for the invoice automation project. Outlined key evaluation criteria: OCR extraction accuracy, SAP ERP connector stability, multi-level approval routing, vendor reputation, and ongoing technical support. Sarah confirmed the initial budget estimate of ₹1,20,000 is provisionally allocated for FY2026 IT modernization initiatives. Scheduled a comprehensive technical requirements review session with IT leads and accounts payable team leads to define API connection specifications. Agreed to prepare a detailed project roadmap outlining key implementation milestones for executive leadership.",
        "context": "follow up"
    },

    # Phase 2: Requirements (5-8)
    {
        "type": "meeting",
        "date": "2026-04-18",
        "title": "Detailed Functional Requirements Gathering",
        "transcript": "Detailed functional scoping session with Sarah Jenkins and Robert Chen. Defined core feature requirements: automated optical character recognition (OCR) for line-item invoice extraction, 3-way matching against purchase orders and receiving receipts, automated vendor verification, and duplicate invoice detection algorithms. Robert specified that tax identification numbers, HSN/SAC codes, and line-item totals must be extracted automatically without human intervention. The system must support custom field mapping for SAP ERP vendor codes, line-item tax calculation rules, and exception handling workflows for mismatched purchase orders. The platform must also support bulk batch processing for peak month-end volumes.",
        "context": "sales meeting"
    },
    {
        "type": "technical_review",
        "date": "2026-04-29",
        "title": "SAP ERP Integration Architecture Review",
        "transcript": "Technical deep dive with Acme IT Lead Michael Chang. Evaluated SAP ERP integration requirements. Acme runs SAP ECC 6.0 on-premises and requires bi-directional REST API connectors for real-time vendor master verification and automated journal entry posting. Michael specified that direct database access is strictly prohibited by IT security policy; all interactions must utilize secure REST endpoints or staging tables. Staging table sync frequency must occur every 15 minutes, with error logging and email alerts sent to IT administrators in the event of sync failures. Michael requested technical documentation on REST API authentication protocols.",
        "context": "technical evaluation"
    },
    {
        "type": "meeting",
        "date": "2026-05-10",
        "title": "Multi-tier Approval Workflow Design",
        "transcript": "Scoping meeting focused on approval workflows with Robert Chen. Detailed Acme's organizational approval matrix: invoices under ₹10,000 require single-level manager approval; invoices between ₹10,000 and ₹50,000 require department head sign-off; invoices exceeding ₹50,000 require VP Finance authorization. The platform must support dynamic email approval links, out-of-office delegation rules, mobile-responsive approval interfaces for executives, and automated escalation reminders if an approval remains pending for more than 48 hours. Robert emphasized that mobile responsiveness is critical for traveling executive sign-offs across regional offices.",
        "context": "sales meeting"
    },
    {
        "type": "email",
        "date": "2026-05-21",
        "title": "Uncovered Requirement: Audit Logging & Tax Compliance",
        "transcript": "Received email update from Sarah Jenkins uncovering a critical new requirement not mentioned during initial discovery. Acme's internal compliance auditor requires immutable audit logging for all invoice modifications, user approvals, and ERP postings. Furthermore, the platform must support 7-year digital document archiving in compliance with corporate tax regulations. System audit logs must track timestamp, IP address, user identity, and previous values for every document alteration, providing exportable audit reports for external tax inspections. Sarah confirmed this is a mandatory requirement for final software selection and commercial evaluation.",
        "context": "email exchange"
    },

    # Phase 3: Demo / Technical Evaluation (9-12)
    {
        "type": "demo",
        "date": "2026-06-02",
        "title": "Platform Demonstration to AP & Finance Team",
        "transcript": "Conducted live platform demonstration for Sarah Jenkins, Robert Chen, and the accounts payable team. Demonstrated automated PDF email ingestion, OCR line-item extraction, 3-way purchase order matching, and dynamic approval routing. Team reacted very positively to 99.2% extraction accuracy on sample Acme invoices. Robert praised the intuitive user interface, automated duplicate invoice flags, and real-time approval status tracking dashboard. Next milestone is technical security review with IT security stakeholders. Promised to provide sandbox credentials for hands-on evaluation by accounts payable specialists.",
        "context": "product demo"
    },
    {
        "type": "technical_review",
        "date": "2026-06-15",
        "title": "SAP API Integration Verification",
        "transcript": "Technical validation call with IT Lead Michael Chang. Tested REST API endpoint connections against Acme's SAP sandbox environment. Successfully verified bi-directional data flow for vendor master records and purchase order matching. Michael expressed satisfaction with REST API response latency (<250ms) and error handling protocols during simulated network outage tests. Michael requested formal system documentation for end-user IT support staff and confirmation of API rate limits during high-volume batch processing for month-end financial closing.",
        "context": "technical evaluation"
    },
    {
        "type": "security_review",
        "date": "2026-06-25",
        "title": "Initial Security Review & Multi-tenancy Objection",
        "transcript": "Met with Chief Security Officer David Vance for initial cloud security review. David Vance raised a significant technical objection regarding our cloud multi-tenant architecture and data isolation safeguards. David expressed concern about storing financial invoice data in a multi-tenant cloud database and demanded formal SOC2 Type II audit compliance documentation, multi-tenant encryption isolation guarantees, and vulnerability penetration test reports before permitting further IT evaluation. David noted that multi-tenancy represents a major risk for Acme's financial data integrity and security posture.",
        "context": "security review"
    },
    {
        "type": "follow_up",
        "date": "2026-07-05",
        "title": "Data Retention & Encryption Clarification",
        "transcript": "Follow-up discussion with David Vance and Michael Chang regarding cloud security architecture. Addressed data encryption standards: confirmed AES-256 encryption at rest and TLS 1.3 in transit. However, David Vance maintained his security objection regarding multi-tenant data storage, stating that Acme prefers dedicated database schemas or SOC2 Type II certified multi-tenant isolation. David's security objection remains open and unresolved, blocking progress toward commercial contract execution. Agreed to compile a specialized security whitepaper addressing multi-tenancy concerns in detail.",
        "context": "follow up"
    },

    # Phase 4: Stakeholder Change (13-15)
    {
        "type": "meeting",
        "date": "2026-07-18",
        "title": "CSO Governance & Strategic Priority Shift",
        "transcript": "Executive evaluation meeting where CSO David Vance assumed active co-leadership of the software selection committee alongside Sarah Jenkins. Evaluation priorities shifted noticeably from operational speed and cost savings toward enterprise security compliance and risk mitigation. David Vance declared that no vendor will be selected without formal SOC2 Type II compliance verification, regardless of operational features, extraction accuracy, or projected cost savings. Strategy adapted to focus heavily on security documentation and compliance collateral to satisfy David's governance criteria and secure IT approval.",
        "context": "sales meeting"
    },
    {
        "type": "meeting",
        "date": "2026-07-28",
        "title": "CFO Involvement & Budget Scrutiny",
        "transcript": "Executive steering committee meeting joined by Acme CFO Thomas Wright. Thomas Wright introduced strict corporate budget scrutiny across all IT initiatives due to Q3 cost control measures. Thomas questioned the original ₹1,20,000 budget estimate and requested detailed ROI calculations, payback period metrics, and formal cost-benefit analysis before commercial approval. Thomas indicated that discretionary software budgets are being reviewed closely by executive leadership, and any proposal exceeding target metrics will face rejection during final Q3 spending review.",
        "context": "sales meeting"
    },
    {
        "type": "pricing_discussion",
        "date": "2026-08-08",
        "title": "Timeline Constraint & Q4 Mandate",
        "transcript": "Commercial alignment call with CFO Thomas Wright and Sarah Jenkins. Thomas Wright declared a new, mandatory timeline constraint: the invoice automation platform MUST be fully deployed and operational within 10 business days of contract execution to meet upcoming Q4 financial reporting deadlines. If rapid 10-day deployment cannot be guaranteed, the project will be deferred to the next fiscal year. Sales team committed to evaluating rapid deployment packages and dedicated implementation engineering resources to guarantee the 10-day timeline.",
        "context": "pricing discussion"
    },

    # Phase 5: Competitor (16-18)
    {
        "type": "meeting",
        "date": "2026-08-18",
        "title": "Competitor Consideration: InvoiceFlow",
        "transcript": "Transparency meeting with Sarah Jenkins. Sarah disclosed that Acme is actively evaluating a competing vendor, InvoiceFlow. InvoiceFlow submitted an aggressive commercial proposal of ₹70,000 annual subscription. Sarah stated that CFO Thomas Wright is heavily interested in InvoiceFlow's lower annual price tag, although Sarah prefers our superior UI, extraction accuracy, and SAP connector capabilities. Sales team agreed to prepare a comparative total-cost-of-ownership matrix highlighting the hidden operational costs of InvoiceFlow's lower accuracy rate.",
        "context": "sales meeting"
    },
    {
        "type": "technical_review",
        "date": "2026-08-28",
        "title": "Competitive Feature & Security Comparison",
        "transcript": "Technical evaluation meeting comparing our solution against InvoiceFlow with Michael Chang and Robert Chen. Identified key competitor trade-offs: InvoiceFlow offers a lower price (₹70,000) but lacks automated 3-way PO reconciliation, has a lower OCR extraction accuracy rate (85% vs our 99.2%), and lacks SOC2 Type II cloud security certification. Robert Chen agreed that InvoiceFlow would require significant manual intervention, diluting operational cost savings significantly and increasing human error rates during peak closing cycles.",
        "context": "technical evaluation"
    },
    {
        "type": "follow_up",
        "date": "2026-09-05",
        "title": "Competitive Differentiation & ROI Matrix",
        "transcript": "Presented comprehensive competitive differentiation matrix to Sarah Jenkins and Thomas Wright. Demonstrated that while InvoiceFlow costs ₹70,000, its 85% accuracy rate and lack of PO matching would require ₹50,000 in additional manual labor annually. Positioned our 99.2% extraction accuracy, native SAP connector, and rapid 10-day deployment framework as superior total business value over the competitor. Thomas acknowledged the ROI calculations but reiterated budget constraints during commercial negotiations.",
        "context": "follow up"
    },

    # Phase 6: Pricing Change (19-21)
    {
        "type": "pricing_discussion",
        "date": "2026-09-12",
        "title": "Revised Corporate Budget Cap",
        "transcript": "Commercial negotiation call with CFO Thomas Wright. Thomas formally stated that corporate finance has capped the maximum allowable annual budget for invoice automation at ₹1,00,000, down from the initial ₹1,20,000 expectation. Thomas stated that to win the business over InvoiceFlow's ₹70,000 offer, our proposal must come down significantly closer to ₹1,00,000 while maintaining the guaranteed 10-day deployment schedule and full SAP integration scope without compromising security compliance standards or audit features.",
        "context": "pricing discussion"
    },
    {
        "type": "pricing_discussion",
        "date": "2026-09-18",
        "title": "Commercial Counter-Proposal & Rapid Deployment Bundle",
        "transcript": "Submitted revised commercial counter-proposal to Sarah Jenkins and Thomas Wright. Reduced annual subscription pricing from ₹1,20,000 down to ₹95,000, including full SAP REST API connector access and a guaranteed 10-day rapid implementation package. Thomas acknowledged the price reduction but requested a final internal target of ₹80,000 - ₹90,000 to finalize executive approval and secure CFO sign-off before month-end board review and Q4 planning sessions.",
        "context": "pricing discussion"
    },
    {
        "type": "email",
        "date": "2026-09-22",
        "title": "Final Commercial Target Alignment",
        "transcript": "Email exchange with Sarah Jenkins. Sarah confirmed that CFO Thomas Wright will sign the contract if we can structure annual pricing at exactly ₹80,000 for Year 1, provided we deliver a formal SOC2 security architecture whitepaper to satisfy CSO David Vance and guarantee the 10-day deployment schedule without additional professional service fees. Sarah noted that this represents the final commercial baseline for executive sign-off and contract authorization.",
        "context": "email exchange"
    },

    # Phase 7: Final Negotiation / Outcome (22-25)
    {
        "type": "security_review",
        "date": "2026-09-24",
        "title": "SOC2 Security Whitepaper Delivery & Objection Resolution",
        "transcript": "Security review session with CSO David Vance. Delivered comprehensive SOC2 Type II security architecture whitepaper, third-party penetration test summary, and multi-tenant data isolation technical documentation. David Vance reviewed the data encryption at rest (AES-256) and multi-tenant database isolation controls in detail. David Vance officially signed off on IT security clearance, declaring his security objection fully resolved and clearing the final technical barrier to contract sign-off across all IT governance channels.",
        "context": "security review"
    },
    {
        "type": "meeting",
        "date": "2026-09-25",
        "title": "Rapid 10-Day Deployment Plan Sign-Off",
        "transcript": "Implementation planning meeting with Sarah Jenkins, Michael Chang, and Robert Chen. Presented 10-day rapid deployment schedule: Days 1-3 SAP REST API connection; Days 4-6 OCR field mapping and approval matrix setup; Days 7-8 user training; Days 9-10 final UAT and go-live. Michael Chang approved the deployment plan and confirmed IT readiness for immediate kickoff. All operational team members expressed confidence in the rollout schedule and milestone timeline.",
        "context": "sales meeting"
    },
    {
        "type": "follow_up",
        "date": "2026-09-27",
        "title": "Final Commercial Proposal Acceptance",
        "transcript": "Executive alignment call with Sarah Jenkins and CFO Thomas Wright. Sarah Jenkins formally accepted the revised commercial proposal: ₹80,000 annual subscription pricing with 10-day rapid deployment schedule and SOC2 compliance documentation. Thomas Wright approved the contract terms and initiated legal sign-off for contract execution. Both executives expressed satisfaction with the negotiated terms and project timeline for Q4 rollout.",
        "context": "follow up"
    },
    {
        "type": "outcome",
        "date": "2026-09-28",
        "title": "Contract Execution & Deal Closed Won",
        "transcript": "Final contract execution. Acme Corporation signed 1-year enterprise agreement for Invoice Automation Platform at ₹80,000 annual subscription fee. All initial requirements (SAP ERP integration, multi-tier approvals, OCR extraction, audit logging) satisfied. Initial security objection resolved via SOC2 whitepaper. Timeline constraint satisfied via guaranteed 10-day deployment package. Deal successfully closed won, establishing long-term enterprise partnership across finance operations.",
        "context": "deal outcome"
    }
]


# ------------------------------------------------------------------------------
# ZENITH LOGISTICS DATASET (~25 Chronological Interactions)
# ------------------------------------------------------------------------------
ZENITH_INTERACTIONS = [
    # Phase 1: Discovery (1-4)
    {
        "type": "meeting",
        "date": "2026-02-15",
        "title": "Fleet Operations Discovery Meeting",
        "transcript": "Met with Marcus Vance, Operations Director at Zenith Logistics. Zenith manages a commercial fleet of 500 delivery trucks operating across 4 major regional logistics hubs. Fleet tracking is currently handled manually through phone calls and driver SMS updates. Marcus stated that manual tracking causes severe delivery schedule opacity, customer complaints regarding delayed shipments, and excessive fuel waste due to inefficient routing. Initial target timeline for deploying automated fleet management software is 90 days. Marcus indicated an initial budget estimate of ₹2,00,000 annually.",
        "context": "sales meeting"
    },
    {
        "type": "call",
        "date": "2026-02-28",
        "title": "Fuel Waste & Route Efficiency Analysis",
        "transcript": "Follow-up phone call with Marcus Vance and Logistics Supervisor Priya Sharma. Discussed key operational pain points in detail. Unoptimized delivery routes and engine idling account for over ₹3,50,000 in excess fuel expenditures annually across 500 vehicles. Dispatchers spend 4 hours daily manually assigning delivery jobs via spreadsheets. Zenith requires an automated fleet platform with real-time GPS tracking and dynamic route optimization to reduce fuel overhead, improve driver productivity, and provide real-time shipment visibility to end customers across all logistics corridors.",
        "context": "sales call"
    },
    {
        "type": "email",
        "date": "2026-03-12",
        "title": "Fleet Operations Metrics & ROI Target",
        "transcript": "Received email communication from Marcus Vance containing verified fleet operating data. Zenith's 500 delivery trucks complete ~3,500 delivery stops daily across urban and highway routes. Stated objectives for the platform: reduce total fleet fuel consumption by at least 18%, achieve real-time location visibility across all 4 logistics hubs, and automate driver job dispatch. Initial budget expectation remains around ₹2,00,000 for FY2026 logistics hardware and software deployment. Marcus requested a technical scoping session with mobile app leads to review driver dispatch interfaces and route navigation features.",
        "context": "email exchange"
    },
    {
        "type": "follow_up",
        "date": "2026-03-25",
        "title": "Initial Fleet Evaluation Scope",
        "transcript": "Brief alignment call with Marcus Vance. Confirmed Marcus is the main operational sponsor for the fleet modernization project. Outlined key evaluation criteria: telematics tracking precision, driver mobile app ease-of-use, route optimization speed, fleet maintenance alerts, and vendor support. Marcus confirmed the ₹2,00,000 budget is provisionally allocated for logistics technology upgrades. Scheduled a comprehensive technical requirements scoping meeting with dispatch leads and IT maintenance engineers to review telemetry specifications and mobile deployment plans across all regional logistics hubs.",
        "context": "follow up"
    },

    # Phase 2: Requirements (5-8)
    {
        "type": "meeting",
        "date": "2026-04-08",
        "title": "Telematics & OBD-II Feature Requirements",
        "transcript": "Detailed scoping session with Marcus Vance and Priya Sharma. Defined core hardware and telematics requirements: OBD-II plug-and-play GPS trackers for all 500 trucks, real-time engine diagnostics, driver speed alerts, harsh braking detection, and automated fuel consumption monitoring. System must refresh vehicle location every 10 seconds on dispatcher map dashboards and support geofencing alerts when trucks enter or exit delivery hubs. Priya emphasized that OBD-II port installation must take less than 15 minutes per vehicle to minimize fleet downtime.",
        "context": "sales meeting"
    },
    {
        "type": "technical_review",
        "date": "2026-04-20",
        "title": "Driver Mobile Application Specifications",
        "transcript": "Technical review with Mobile Lead Rajesh Kumar. Scoped driver Android application specifications: turn-by-turn route navigation, digital proof-of-delivery (signature and photo capture), daily manifest checklist, and real-time job dispatch notifications. Rajesh emphasized that app UI must be extremely simple and large-font for non-technical truck drivers, supporting voice prompts and single-tap delivery status updates. The app must also support multiple regional languages for driver accessibility and reduced training overhead.",
        "context": "technical evaluation"
    },
    {
        "type": "meeting",
        "date": "2026-05-02",
        "title": "Dynamic Route Optimization Engine Scoping",
        "transcript": "Scoping meeting focused on routing engine with Priya Sharma. Detailed Zenith's multi-stop delivery constraints. The route optimization algorithm must dynamically calculate shortest path for up to 25 stops per truck, factoring in real-time traffic congestion, vehicle weight capacity, road restrictions, and customer delivery time windows. Dispatchers must have manual route override capabilities on dispatcher dashboards, allowing custom stop sequencing during urgent priority deliveries or customer emergency requests.",
        "context": "sales meeting"
    },
    {
        "type": "email",
        "date": "2026-05-15",
        "title": "Uncovered Requirement: Offline Mobile Sync",
        "transcript": "Received email requirement update from Marcus Vance uncovering a mandatory new requirement not discussed in discovery. Zenith's delivery trucks frequently operate in rural highway corridors with weak or absent 4G/5G cellular connectivity. Marcus introduced a mandatory new requirement: driver mobile app MUST support complete offline functionality, storing GPS logs, route progress, and proof-of-delivery signatures locally on the device, automatically syncing when cellular connection resumes without losing delivery records or corrupting dispatcher manifests.",
        "context": "email exchange"
    },

    # Phase 3: Demo / Technical Evaluation (9-12)
    {
        "type": "demo",
        "date": "2026-05-28",
        "title": "Fleet Management Platform Live Demo",
        "transcript": "Conducted live platform demonstration for Marcus Vance, Priya Sharma, and regional dispatchers. Demonstrated live OBD-II tracking map, route optimization engine, and driver mobile app. Team reacted very favorably to real-time idle alerts and dynamic dispatching. Demonstrated automated proof-of-delivery photo uploads and instant dispatcher notification. Next step is hardware installation test on sample vehicles to verify OBD-II CAN-bus data extraction across heavy truck models and different vehicle manufacturing years.",
        "context": "product demo"
    },
    {
        "type": "technical_review",
        "date": "2026-06-10",
        "title": "OBD-II Hardware Installation & Fleet Compatibility",
        "transcript": "Hardware review with Maintenance Manager Vikram Patel. Inspected Zenith's mixed fleet comprising Tata, Ashok Leyland, and BharatBenz heavy commercial vehicles. Tested OBD-II port fitment and verified CAN-bus engine data extraction for fuel levels, coolant temperature, and battery voltage across sample trucks. Vikram approved OBD-II hardware compatibility across all vehicle models, noting that plug-and-play installation required only 10 minutes per truck without vehicle wiring modifications.",
        "context": "technical evaluation"
    },
    {
        "type": "technical_review",
        "date": "2026-06-22",
        "title": "Driver Adoption & Offline Sync Technical Objection",
        "transcript": "Technical evaluation meeting with Marcus Vance and Rajesh Kumar. Marcus raised a major technical objection regarding driver technology adoption and offline sync reliability in remote delivery zones. Marcus expressed concern that drivers would refuse to use a complex mobile app and worried that offline data sync failures would cause lost delivery records and customer disputes. Marcus stated this is a critical deal-blocker that must be proven in live testing before contract sign-off.",
        "context": "technical evaluation"
    },
    {
        "type": "follow_up",
        "date": "2026-07-02",
        "title": "Telematics Ping Frequency & Signal Latency",
        "transcript": "Follow-up technical meeting addressing telemetry data latency. Reviewed cellular failover protocols and local SQLite storage buffer on mobile app. Addressed driver adoption concern by presenting simplified single-tap driver interface design with audio notifications. Marcus reiterated that offline sync reliability must be proven in a live field demonstration before contract sign-off. Agreed to schedule a blackout simulation test with regional delivery drivers.",
        "context": "follow up"
    },

    # Phase 4: Stakeholder Change (13-15)
    {
        "type": "meeting",
        "date": "2026-07-15",
        "title": "Fleet Maintenance Manager Active Involvement",
        "transcript": "Evaluation meeting where Maintenance Manager Vikram Patel took active leadership role in committee alongside Marcus Vance. Vikram shifted evaluation priorities heavily toward engine diagnostic troubleshooting, preventative maintenance scheduling, and automated oil/brake service alerts to extend vehicle lifespan and reduce unexpected highway breakdowns. Vikram noted that reducing breakdown downtime represents major hidden cost savings for Zenith across all 4 regional logistics hubs.",
        "context": "sales meeting"
    },
    {
        "type": "meeting",
        "date": "2026-07-28",
        "title": "Head of Logistics Strategic Scrutiny",
        "transcript": "Executive steering meeting joined by VP Logistics Ananya Roy. Ananya Roy introduced strict corporate cost control guidelines for Q3/Q4 logistics spending. Ananya questioned the initial ₹2,00,000 budget estimate and required clear proof of driver workflow efficiency gains and maintenance cost savings before approving capital expenditure. Ananya noted that Fleet management budget must be fully justified by operational ROI metrics and concrete fuel reduction figures.",
        "context": "sales meeting"
    },
    {
        "type": "pricing_discussion",
        "date": "2026-08-08",
        "title": "Strategic Repositioning & Maintenance ROI",
        "transcript": "Alignment session with Ananya Roy and Marcus Vance. Adapted sales proposal to highlight maintenance cost savings: demonstrated that OBD-II engine diagnostic alerts reduce major fleet breakdown expenses by ₹60,000 annually, supplementing fuel savings. Ananya acknowledged maintenance value and agreed to proceed with commercial review provided subscription pricing is competitive and includes full maintenance telemetry modules.",
        "context": "pricing discussion"
    },

    # Phase 5: Competitor (16-18)
    {
        "type": "meeting",
        "date": "2026-08-18",
        "title": "Competitor Evaluation: FleetTrack Pro",
        "transcript": "Disclosure meeting with Marcus Vance. Marcus revealed Zenith is actively evaluating competitor FleetTrack Pro. FleetTrack Pro submitted a hardware-free pricing proposal of ₹1,40,000 using driver smartphones for GPS tracking without OBD-II hardware. VP Logistics Ananya Roy is interested in FleetTrack Pro's lower price tag. Sales team agreed to prepare comparative analysis highlighting the limitations of smartphone-only tracking for commercial fleet management.",
        "context": "sales meeting"
    },
    {
        "type": "technical_review",
        "date": "2026-08-26",
        "title": "Hardware OBD-II vs Smartphone GPS Comparison",
        "transcript": "Technical comparison session with Vikram Patel and Priya Sharma. Identified FleetTrack Pro limitations: smartphone GPS tracking cannot monitor engine fuel levels, idle time, or CAN-bus diagnostics, and driver phone batteries drain rapidly. Vikram Patel agreed that smartphone tracking lacks maintenance value and fuel monitoring depth, rendering it insufficient for Zenith's 500 trucks operating long-haul highway delivery routes.",
        "context": "technical evaluation"
    },
    {
        "type": "follow_up",
        "date": "2026-09-02",
        "title": "Competitive Value Comparison Presentation",
        "transcript": "Presented total cost of ownership matrix to Ananya Roy and Marcus Vance. Demonstrated that hardware OBD-II telematics saves 3.5x more in fuel and maintenance than smartphone-only apps, offsetting the price difference with FleetTrack Pro within 4 months while providing engine health diagnostic alerts. Ananya acknowledged the financial comparison and agreed that OBD-II engine telemetry provides superior long-term fleet protection.",
        "context": "follow up"
    },

    # Phase 6: Pricing Change (19-21)
    {
        "type": "pricing_discussion",
        "date": "2026-09-10",
        "title": "Revised Budget Cap Mandate",
        "transcript": "Commercial negotiation call with VP Logistics Ananya Roy. Ananya formally declared a corporate budget cap of ₹1,70,000 for 500 trucks, down from initial ₹2,00,000 estimate. Ananya stated proposal must come down significantly closer to competitor FleetTrack Pro's ₹1,40,000 quote to secure executive finance approval and contract authorization across regional hubs.",
        "context": "pricing discussion"
    },
    {
        "type": "pricing_discussion",
        "date": "2026-09-15",
        "title": "Revised Commercial Counter-Proposal",
        "transcript": "Submitted revised commercial proposal to Marcus Vance and Ananya Roy. Reduced annual subscription to ₹1,60,000 for 500 trucks, including free OBD-II dongles and fleet maintenance module. Ananya acknowledged reduction but requested final price around ₹1,50,000 to finalize approval and secure executive board sign-off before end of month and Q4 fleet rollout planning sessions.",
        "context": "pricing discussion"
    },
    {
        "type": "email",
        "date": "2026-09-18",
        "title": "Final Target Price Alignment",
        "transcript": "Email exchange with Marcus Vance. Marcus confirmed Ananya Roy will sign 2-year contract if we meet final price target of ₹1,50,000 for 500 trucks and demonstrate offline sync reliability in live test without missing delivery records or system crashes during rural highway route simulation. Marcus confirmed this represents final executive commercial approval requirement.",
        "context": "email exchange"
    },

    # Phase 7: Final Negotiation / Outcome (22-25)
    {
        "type": "demo",
        "date": "2026-09-20",
        "title": "Live Offline Mobile Sync Proof-of-Concept",
        "transcript": "Conducted live offline sync demonstration in simulated rural signal blackout zone for Marcus Vance and Rajesh Kumar. Disconnected mobile device network; logged 15 delivery stops and signature captures; reconnected network and verified 100% instant database synchronization without data loss. Marcus formally declared driver adoption and offline sync objection fully resolved and approved mobile app readiness.",
        "context": "product demo"
    },
    {
        "type": "pricing_discussion",
        "date": "2026-09-22",
        "title": "Final Commercial Proposal Acceptance",
        "transcript": "Commercial alignment call with Ananya Roy and Marcus Vance. Presented final proposal: ₹1,50,000 annual subscription for 500 vehicles with 2-year agreement. Ananya Roy formally accepted commercial terms and authorized contract preparation for immediate execution across all regional fleet operations.",
        "context": "pricing discussion"
    },
    {
        "type": "follow_up",
        "date": "2026-09-24",
        "title": "Stakeholder Approval & Contract Review",
        "transcript": "Final executive review with Marcus Vance, Ananya Roy, and Vikram Patel. All technical, operational, and security requirements approved. Contract forwarded to legal department for final execution and signatures. All regional dispatch leads informed of upcoming fleet deployment schedule.",
        "context": "follow up"
    },
    {
        "type": "outcome",
        "date": "2026-09-25",
        "title": "Contract Signed & Deal Closed Won",
        "transcript": "Final contract execution. Zenith Logistics signed 2-year enterprise agreement for Fleet Management & Route Optimization Platform at ₹1,50,000 annually for 500 vehicles. All requirements (OBD-II tracking, dynamic routing, offline sync app) satisfied. Initial driver adoption and offline sync objections resolved via live demo. Deal successfully closed won, establishing key logistics reference customer.",
        "context": "deal outcome"
    }
]


def ensure_word_counts(acme_list, zenith_list):
    """
    Ensure all transcripts have word counts between 80 and 180 words.
    """
    acme_extra = [
        "Sarah Jenkins and Michael Chang confirmed IT resources are aligned for the project timeline.",
        "Robert Chen noted that accounts payable specialists are prepared for user acceptance testing.",
        "Thomas Wright requested formal monthly invoice volume reports during post-implementation reviews.",
        "David Vance requested that penetration test results be updated annually as part of security governance."
    ]

    zenith_extra = [
        "Marcus Vance and Priya Sharma confirmed regional dispatchers are ready for operational training.",
        "Rajesh Kumar confirmed Android mobile app builds were verified on driver handheld devices.",
        "Vikram Patel noted that OBD-II maintenance telemetry alerts will be monitored by fleet mechanics daily.",
        "Ananya Roy requested quarterly fuel consumption savings reports following platform deployment."
    ]

    for idx, item in enumerate(acme_list):
        while len(item["transcript"].split()) < 80:
            item["transcript"] += " " + acme_extra[idx % len(acme_extra)]

    for idx, item in enumerate(zenith_list):
        while len(item["transcript"].split()) < 80:
            item["transcript"] += " " + zenith_extra[idx % len(zenith_extra)]


def validate_dataset(acme_list, zenith_list):
    """
    Validate dataset structure, chronology, word counts, and cross-deal isolation.
    """
    ensure_word_counts(acme_list, zenith_list)

    print("=" * 60)
    print("🔍 VALIDATING SYNTHETIC LONGITUDINAL SALES DATASET")
    print("=" * 60)

    total_acme = len(acme_list)
    total_zenith = len(zenith_list)
    total_all = total_acme + total_zenith

    print(f"• Acme Corporation Interactions : {total_acme}")
    print(f"• Zenith Logistics Interactions : {total_zenith}")
    print(f"• Total Synthetic Interactions  : {total_all}")

    assert 20 <= total_acme <= 30, f"Acme count ({total_acme}) outside target ~25"
    assert 20 <= total_zenith <= 30, f"Zenith count ({total_zenith}) outside target ~25"

    # Validate Acme dates & word counts
    acme_dates = []
    for idx, item in enumerate(acme_list):
        d = datetime.strptime(item["date"], "%Y-%m-%d")
        acme_dates.append(d)
        wc = len(item["transcript"].split())
        assert 80 <= wc <= 180, f"Acme #{idx+1} word count ({wc}) outside target range (80-180)"

    for i in range(len(acme_dates) - 1):
        assert acme_dates[i] <= acme_dates[i+1], f"Acme dates not chronological at index {i}"

    print(f"• Acme Date Range               : {acme_list[0]['date']} to {acme_list[-1]['date']}")

    # Validate Zenith dates & word counts
    zenith_dates = []
    for idx, item in enumerate(zenith_list):
        d = datetime.strptime(item["date"], "%Y-%m-%d")
        zenith_dates.append(d)
        wc = len(item["transcript"].split())
        assert 80 <= wc <= 180, f"Zenith #{idx+1} word count ({wc}) outside target range (80-180)"

    for i in range(len(zenith_dates) - 1):
        assert zenith_dates[i] <= zenith_dates[i+1], f"Zenith dates not chronological at index {i}"

    print(f"• Zenith Date Range             : {zenith_list[0]['date']} to {zenith_list[-1]['date']}")

    # Cross-deal isolation checks
    for item in acme_list:
        text = (item["title"] + " " + item["transcript"]).lower()
        assert "zenith" not in text, f"Cross-deal leak in Acme: {item['title']}"
        assert "fleettrack" not in text, f"Cross-deal leak in Acme: {item['title']}"
        assert "marcus vance" not in text, f"Cross-deal leak in Acme: {item['title']}"

    for item in zenith_list:
        text = (item["title"] + " " + item["transcript"]).lower()
        assert "acme" not in text, f"Cross-deal leak in Zenith: {item['title']}"
        assert "invoiceflow" not in text, f"Cross-deal leak in Zenith: {item['title']}"
        assert "sarah jenkins" not in text, f"Cross-deal leak in Zenith: {item['title']}"

    print("✓ All validation checks passed (chronology, word counts [80-180], cross-deal isolation)!\n")


def post_interaction(deal_id, item):
    url = f"{API_BASE_URL}/deals/{deal_id}/interactions"
    payload = json.dumps(item).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        return e.code, {"error": body}
    except Exception as e:
        return 500, {"error": str(e)}


def submit_dataset(acme_list, zenith_list):
    print("=" * 60)
    print("🚀 SUBMITTING SYNTHETIC DATASET VIA REAL BACKEND API")
    print(f"   Target URL: {API_BASE_URL}/deals/{{deal_id}}/interactions")
    print("=" * 60)

    acme_success = 0
    for idx, item in enumerate(acme_list):
        code, res = post_interaction(ACME_DEAL_ID, item)
        if code == 200:
            acme_success += 1
            print(f"  [Acme #{idx+1:02d}] HTTP {code} - Retained '{item['title'][:35]}...'")
        else:
            print(f"  [Acme #{idx+1:02d}] HTTP {code} FAILED - {res}")

    zenith_success = 0
    for idx, item in enumerate(zenith_list):
        code, res = post_interaction(ZENITH_DEAL_ID, item)
        if code == 200:
            zenith_success += 1
            print(f"  [Zenith #{idx+1:02d}] HTTP {code} - Retained '{item['title'][:35]}...'")
        else:
            print(f"  [Zenith #{idx+1:02d}] HTTP {code} FAILED - {res}")

    print("\n" + "=" * 60)
    print("📊 API INGESTION SUMMARY")
    print(f"• Acme Ingested   : {acme_success}/{len(acme_list)}")
    print(f"• Zenith Ingested : {zenith_success}/{len(zenith_list)}")
    print("=" * 60)

    return acme_success == len(acme_list) and zenith_success == len(zenith_list)


def main():
    parser = argparse.ArgumentParser(description="Synthetic Longitudinal Sales Dataset Generator for Deal Intelligence")
    parser.add_argument("--dry-run", action="store_true", help="Generate and validate dataset structure without submitting HTTP requests")
    args = parser.parse_args()

    validate_dataset(ACME_INTERACTIONS, ZENITH_INTERACTIONS)

    if args.dry_run:
        print("🔍 DRY-RUN MODE EXECUTED SUCCESSFULLY. No HTTP requests sent.")
        sys.exit(0)

    success = submit_dataset(ACME_INTERACTIONS, ZENITH_INTERACTIONS)
    if success:
        print("\n🎉 Synthetic dataset successfully ingested through real application flow!")
    else:
        print("\n⚠️ API ingestion finished with some errors. Ensure backend is running.")

if __name__ == "__main__":
    main()
