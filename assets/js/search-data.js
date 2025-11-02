// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "about",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-wiki",
          title: "wiki",
          description: "Glossary of terms used in power systems",
          section: "Navigation",
          handler: () => {
            window.location.href = "/wiki/";
          },
        },{id: "nav-references",
          title: "references",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/references/";
          },
        },{id: "dropdown-archive",
              title: "archive",
              description: "",
              section: "Dropdown",
              handler: () => {
                window.location.href = "/wiki-tag/";
              },
            },{id: "dropdown-change-log",
              title: "change log",
              description: "",
              section: "Dropdown",
              handler: () => {
                window.location.href = "/changelog/";
              },
            },{id: "wiki-30-minute-reserve-service",
          title: '30-Minute Reserve Service',
          description: "Can be satisfied by online or offline resources that are able to respond in 30 minutes or less.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/30-minute-reserve-service/";
            },},{id: "wiki-adequacy",
          title: 'Adequacy',
          description: "The ability to supply the demand and energy requirements of the end-use customers.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/adequacy/";
            },},{id: "wiki-ambient-adjusted-ratings",
          title: 'Ambient-Adjusted Ratings',
          description: "",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/ambient-adjusted-ratings/";
            },},{id: "wiki-ancillary-services",
          title: 'Ancillary Services',
          description: "Services necessary to support the transmission of electric power.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/ancillary-services/";
            },},{id: "wiki-area-control-error",
          title: 'Area Control Error',
          description: "ACE. The instantaneous difference between net actual and scheduled interchange.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/area-control-error/";
            },},{id: "wiki-automatic-generation-control",
          title: 'Automatic Generation Control',
          description: "AGC. Automatic regulation of the power output of generators.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/automatic-generation-control/";
            },},{id: "wiki-balancing-authority-area",
          title: 'Balancing Authority Area',
          description: "The collection of generation, transmission, and loads within the metered boundaries of the Balancing Authority.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/balancing-authority-area/";
            },},{id: "wiki-balancing-authority",
          title: 'Balancing Authority',
          description: "The responsible entity within a Balancing Authority Area.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/balancing-authority/";
            },},{id: "wiki-bilateral-transaction",
          title: 'Bilateral Transaction',
          description: "A direct contract between a seller and buyer outside of a centralized market.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/bilateral-transaction/";
            },},{id: "wiki-black-start",
          title: 'Black Start',
          description: "Establishing the voltage from around zero",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/black-start/";
            },},{id: "wiki-bulk-electric-system",
          title: 'Bulk Electric System',
          description: "BES. Transmission Elements and Power resources 100 kV or higher.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/bulk-electric-system/";
            },},{id: "wiki-bulk-power-system",
          title: 'Bulk Power System',
          description: "BPS. Facilities and control systems for an transmission network.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/bulk-power-system/";
            },},{id: "wiki-capacity-markets",
          title: 'Capacity Markets',
          description: "A market for trading capacity credits.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/capacity-markets/";
            },},{id: "wiki-cascading",
          title: 'Cascading',
          description: "The uncontrolled successive loss of System Elements triggered by an incident.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/cascading/";
            },},{id: "wiki-co-located-load",
          title: 'Co-Located Load',
          description: "Load connected to the an existing or planned facility.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/co-located-load/";
            },},{id: "wiki-common-format-for-transient-data-exchange",
          title: 'Common Format for Transient Data Exchange',
          description: "COMTRADE. Inactive.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/common-format-for-transient-data-exchange/";
            },},{id: "wiki-common-information-model",
          title: 'Common Information Model',
          description: "CIM. A set of open standards for representing power system components",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/common-information-model/";
            },},{id: "wiki-compliance-factor",
          title: 'Compliance Factor',
          description: "CF.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/compliance-factor/";
            },},{id: "wiki-contingency-analysis",
          title: 'Contingency Analysis',
          description: "Procedures to study a contingency.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/contingency-analysis/";
            },},{id: "wiki-contingency-list",
          title: 'Contingency List',
          description: "A list of network elements to be simulated as disconnected.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/contingency-list/";
            },},{id: "wiki-contingency-reserve-service",
          title: 'Contingency Reserve Service',
          description: "A.k.a. Primary Reserve. Can be satisfied in 10 minutes or less.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/contingency-reserve-service/";
            },},{id: "wiki-contingency-reserve",
          title: 'Contingency Reserve',
          description: "Capacity deployed by the Balancing Authority to meet the Disturbance Control Standard.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/contingency-reserve/";
            },},{id: "wiki-contingency",
          title: 'Contingency',
          description: "The unexpected failure or outage of a system component.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/contingency/";
            },},{id: "wiki-control-area",
          title: 'Control Area',
          description: "A.k.a. Balancing Authority Area.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/control-area/";
            },},{id: "wiki-control-performance-standard-1",
          title: 'Control Performance Standard 1',
          description: "CPS1. A standard that measures impact on frequency error.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/control-performance-standard-1/";
            },},{id: "wiki-control-performance-standard-2",
          title: 'Control Performance Standard 2',
          description: "CPS2. A standard intended to limit unscheduled flows.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/control-performance-standard-2/";
            },},{id: "wiki-converter-driven-stability",
          title: 'Converter-Driven Stability',
          description: "Converter-interfaced generation&#39;s impact on stability.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/converter-driven-stability/";
            },},{id: "wiki-critical-clearing-time",
          title: 'Critical Clearing Time',
          description: "CCT. The maximum permissible duration of the fault.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/critical-clearing-time/";
            },},{id: "wiki-critical-inertia",
          title: 'Critical Inertia',
          description: "Minimum level of system inertia necessary to ensure deployment of frequency responsive reserves.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/critical-inertia/";
            },},{id: "wiki-day-ahead-energy-market",
          title: 'Day Ahead Energy Market',
          description: "Forward markets for electricity to be supplied the following day.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/day-ahead-energy-market/";
            },},{id: "wiki-digital-twin",
          title: 'Digital Twin',
          description: "A virtual representation to reflect a physical object accurately.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/digital-twin/";
            },},{id: "wiki-distributed-energy-resources",
          title: 'Distributed Energy Resources',
          description: "DER. A source of electric power that is not directly connected to a bulk power system.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/distributed-energy-resources/";
            },},{id: "wiki-distribution-factors",
          title: 'Distribution Factors',
          description: "DFAX.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/distribution-factors/";
            },},{id: "wiki-distribution-provider",
          title: 'Distribution Provider',
          description: "Provides and operates the “wires” between the transmission system and the end-use customer.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/distribution-provider/";
            },},{id: "wiki-distribution",
          title: 'Distribution',
          description: "The act of distributing gas or electric power to customers.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/distribution/";
            },},{id: "wiki-disturbance",
          title: 'Disturbance',
          description: "Any perturbation or sudden loss of generation or interruption of load.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/disturbance/";
            },},{id: "wiki-dynamic-line-ratings",
          title: 'Dynamic Line Ratings',
          description: "DLR. A grid enhancing technology (GET) that provides real-time ratings of transmission lines based on current weather conditions.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/dynamic-line-ratings/";
            },},{id: "wiki-economic-dispatch",
          title: 'Economic Dispatch',
          description: "Allocation of generating units for economical production.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/economic-dispatch/";
            },},{id: "wiki-electrical-resonance",
          title: 'Electrical Resonance',
          description: "The behavior of power systems with conventional turbine-generators and variable speed induction generators.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/electrical-resonance/";
            },},{id: "wiki-emergency-rating",
          title: 'Emergency Rating',
          description: "A transmission facility rating that reflects operation for a specified, finite period.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/emergency-rating/";
            },},{id: "wiki-emergency",
          title: 'Emergency',
          description: "Abnormal system condition that requires automatic or immediate manual action.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/emergency/";
            },},{id: "wiki-equal-area-criterion",
          title: 'Equal Area Criterion',
          description: "To determine the maximum permissible increase in mechanical power input for system stability.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/equal-area-criterion/";
            },},{id: "wiki-expected-unserved-energy",
          title: 'Expected Unserved Energy',
          description: "EUE. A measure of the capability to continuously serve loads.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/expected-unserved-energy/";
            },},{id: "wiki-extended-equal-area-criterion",
          title: 'Extended Equal Area Criterion',
          description: "Extend EAC to multi-machine systems.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/extended-equal-area-criterion/";
            },},{id: "wiki-facility-rating",
          title: 'Facility Rating',
          description: "",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/facility-rating/";
            },},{id: "wiki-fast-frequency-response",
          title: 'Fast Frequency Response',
          description: "FFR. Power in response to frequency changes during the arresting phase",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/fast-frequency-response/";
            },},{id: "wiki-fault",
          title: 'Fault',
          description: "An event such as a short circuit, a broken wire, or an intermittent connection.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/fault/";
            },},{id: "wiki-financial-markets",
          title: 'Financial Markets',
          description: "Trading financially settled products.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/financial-markets/";
            },},{id: "wiki-financial-transmission-right",
          title: 'Financial Transmission Right',
          description: "FTR. Compensation contract for transmission charges due to grid congestion.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/financial-transmission-right/";
            },},{id: "wiki-flexibility-reserve",
          title: 'Flexibility Reserve',
          description: "Addressing variability and uncertainty on longer timescales than operating reserves and regulation service.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/flexibility-reserve/";
            },},{id: "wiki-flowgate",
          title: 'Flowgate',
          description: "Portion of the transmission system used to analyze power flow impact.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/flowgate/";
            },},{id: "wiki-frequency-deviation",
          title: 'Frequency Deviation',
          description: "A change in Interconnection frequency.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/frequency-deviation/";
            },},{id: "wiki-frequency-regulation",
          title: 'Frequency Regulation',
          description: "The ability of a Balancing Authority to help maintain Scheduled Frequency.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/frequency-regulation/";
            },},{id: "wiki-frequency-response-measure",
          title: 'Frequency Response Measure',
          description: "The median of all Frequency Response observations reported annually.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/frequency-response-measure/";
            },},{id: "wiki-frequency-response",
          title: 'Frequency Response',
          description: "The ability of a system to react to a change in system frequency.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/frequency-response/";
            },},{id: "wiki-frequency-stability",
          title: 'Frequency Stability',
          description: "The ability of a power system to maintain steady frequency following a severe system upset.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/frequency-stability/";
            },},{id: "wiki-futures-market",
          title: 'Futures Market',
          description: "For contracts for future delivery of a commodity or security.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/futures-market/";
            },},{id: "wiki-generation-redispatch",
          title: 'Generation Redispatch',
          description: "Generators are adjusted away (off-cost) from their normal assignments (on-cost).",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/generation-redispatch/";
            },},{id: "wiki-generation-shift-factor",
          title: 'Generation Shift Factor',
          description: "GSF.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/generation-shift-factor/";
            },},{id: "wiki-interchange",
          title: 'Interchange',
          description: "Energy transfers that cross Balancing Authority boundaries.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/interchange/";
            },},{id: "wiki-interconnection-reliability-operating-limit",
          title: 'Interconnection Reliability Operating Limit',
          description: "A System Operating Limit that, if violated, could lead to instability or cascading outages.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/interconnection-reliability-operating-limit/";
            },},{id: "wiki-interconnection",
          title: 'Interconnection',
          description: "A geographic area where BPS components are synchronized.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/interconnection/";
            },},{id: "wiki-interruptible-demand",
          title: 'Interruptible Demand',
          description: "Customer demand that can be interrupted by control or request of the system operator.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/interruptible-demand/";
            },},{id: "wiki-inverter-based-resources",
          title: 'Inverter-based Resources',
          description: "IBR. BPS-connected resources that have a power electronic interface.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/inverter-based-resources/";
            },},{id: "wiki-line-outage-distribution-factor",
          title: 'Line Outage Distribution Factor',
          description: "LODF.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/line-outage-distribution-factor/";
            },},{id: "wiki-localtional-marginal-price",
          title: 'Localtional Marginal Price',
          description: "LMP. Marginal price for energy at the location delivered or received.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/localtional-marginal-price/";
            },},{id: "wiki-loss-of-load-events",
          title: 'Loss-of-Load Events',
          description: "LOLEV. The number of events in which some system load is not served in a given year.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/loss-of-load-events/";
            },},{id: "wiki-loss-of-load-expectation",
          title: 'Loss-of-Load Expectation',
          description: "LOLE. The number of days per year for which the available generation capacity is insufficient.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/loss-of-load-expectation/";
            },},{id: "wiki-loss-of-load-hour",
          title: 'Loss-of-Load Hour',
          description: "LOLH. The number of hours per year where demand will exceed the generating capacity.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/loss-of-load-hour/";
            },},{id: "wiki-loss-of-load-probability",
          title: 'Loss-of-Load Probability',
          description: "LOLP.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/loss-of-load-probability/";
            },},{id: "wiki-market-power",
          title: 'Market Power',
          description: "The ability to control or affect price.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/market-power/";
            },},{id: "wiki-market-structure",
          title: 'Market Structure',
          description: "The rules, mechanisms, and processes under which a market operates.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/market-structure/";
            },},{id: "wiki-market-unit",
          title: 'Market Unit',
          description: "The unit sets the price of next increment or decrement of energy.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/market-unit/";
            },},{id: "wiki-market",
          title: 'Market',
          description: "A venue where participants buy and sell products or services.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/market/";
            },},{id: "wiki-multi-criteria-decision-analysis-based-metrics",
          title: 'Multi-Criteria Decision Analysis-Based Metrics',
          description: "(MCDA)-Based Metrics.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/multi-criteria-decision-analysis-based-metrics/";
            },},{id: "wiki-non-spinning-reserve",
          title: 'Non-Spinning Reserve',
          description: "Unconnected to the system but capable of serving demand within a specified time.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/non-spinning-reserve/";
            },},{id: "wiki-non-storm-resilience-metric",
          title: 'Non-Storm Resilience Metric',
          description: "A metric focuses on robustness and the ability to withstand events.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/non-storm-resilience-metric/";
            },},{id: "wiki-non-synchronized-reserve",
          title: 'Non-Synchronized Reserve',
          description: "Reserve capability within 10 minutes not electrically synchronized to the system",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/non-synchronized-reserve/";
            },},{id: "wiki-operating-reliability",
          title: 'Operating Reliability',
          description: "The ability to withstand sudden disturbances while avoiding uncontrolled cascading blackouts or damage to equipment.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/operating-reliability/";
            },},{id: "wiki-operating-reserve-spinning",
          title: 'Operating Reserve – Spinning',
          description: "Generation synchronized to the system and fully available to serve load within the Disturbance Recovery Period.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/operating-reserve-spinning/";
            },},{id: "wiki-operating-reserve-supplemental",
          title: 'Operating Reserve – Supplemental',
          description: "Generation or load available to serve load within the Disturbance Recovery Period.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/operating-reserve-supplemental/";
            },},{id: "wiki-operating-reserve",
          title: 'Operating Reserve',
          description: "Capability above firm system demand required for regulation, load forecasting error, and outages.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/operating-reserve/";
            },},{id: "wiki-oscillation",
          title: 'Oscillation',
          description: "A repetitive motion that can be either undamped, positively damped, or negatively damped.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/oscillation/";
            },},{id: "wiki-outage-transfer-distribution-factor",
          title: 'Outage Transfer Distribution Factor',
          description: "OTDF.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/outage-transfer-distribution-factor/";
            },},{id: "wiki-participation-factors",
          title: 'Participation Factors',
          description: "One definition is about dispath and another is about small-signal stability.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/participation-factors/";
            },},{id: "wiki-performance-based-metrics",
          title: 'Performance-Based Metrics',
          description: "A.k.a. consequence-based metrics. Quantitative approaches for assessing system resilience.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/performance-based-metrics/";
            },},{id: "wiki-power-transfer-distribution-factor",
          title: 'Power Transfer Distribution Factor',
          description: "PTDF.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/power-transfer-distribution-factor/";
            },},{id: "wiki-primary-control",
          title: 'Primary Control',
          description: "A.k.a. Frequency Response.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/primary-control/";
            },},{id: "wiki-primary-frequency-response",
          title: 'Primary Frequency Response',
          description: "PFR. Immediate proportional response to system Frequency Deviations.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/primary-frequency-response/";
            },},{id: "wiki-ramp",
          title: 'Ramp',
          description: "A.k.a. Ramp Rate. The rate at which the interchange schedule or generator output is attained.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/ramp/";
            },},{id: "wiki-real-time-energy-market",
          title: 'Real Time Energy Market',
          description: "Use dispatch run to determine the least cost solution to balance supply and demand.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/real-time-energy-market/";
            },},{id: "wiki-real-time-reliability-model",
          title: 'Real-Time Reliability Model',
          description: "A.k.a. EMS model. A computer representation of the power system facilities.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/real-time-reliability-model/";
            },},{id: "wiki-region",
          title: 'Region',
          description: "Bulk power system reliability regions in North America.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/region/";
            },},{id: "wiki-regulating-reserve",
          title: 'Regulating Reserve',
          description: "Reserve for AGC to provide normal regulating margin.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/regulating-reserve/";
            },},{id: "wiki-reliability-coordinator-area",
          title: 'Reliability Coordinator Area',
          description: "The collection of generation, transmission, and loads within the boundaries of the Reliability Coordinator.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/reliability-coordinator-area/";
            },},{id: "wiki-reliability",
          title: 'Reliability',
          description: "The probability of satisfactory operation of a power system over the long run.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/reliability/";
            },},{id: "wiki-remedial-action-scheme",
          title: 'Remedial Action Scheme',
          description: "RAS.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/remedial-action-scheme/";
            },},{id: "wiki-reserve-markets",
          title: 'Reserve Markets',
          description: "A market-based system for the purchase and sale of the Reserves.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/reserve-markets/";
            },},{id: "wiki-reserve",
          title: 'Reserve',
          description: "The generating capability that is “standing by” ready for service in the event that something happens on the power system.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/reserve/";
            },},{id: "wiki-resilience",
          title: 'Resilience',
          description: "The ability to withstand and reduce the magnitude and/or duration of disruptive events.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/resilience/";
            },},{id: "wiki-resonance-stability",
          title: 'Resonance Stability',
          description: "The behavior of power systems under oscillatory energy exchange conditions.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/resonance-stability/";
            },},{id: "wiki-resource-scheduling-amp-commitment",
          title: 'Resource Scheduling &amp;amp; Commitment',
          description: "RSC. Security-constrained resource commitment.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/resource-scheduling-commitment/";
            },},{id: "wiki-response-rate",
          title: 'Response Rate',
          description: "The Ramp Rate that a generating unit can achieve under normal conditions.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/response-rate/";
            },},{id: "wiki-ride-through",
          title: 'Ride-through',
          description: "Ability to withstand voltage or frequency disturbances and continue operating.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/ride-through/";
            },},{id: "wiki-rotating-blackouts",
          title: 'Rotating Blackouts',
          description: "When each set of distribution feeders is interrupted for a limited time and then rotated among individual feeders.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/rotating-blackouts/";
            },},{id: "wiki-rotor-angle-stability",
          title: 'Rotor Angle Stability',
          description: "The ability to remain in synchronism under normal and disturbed conditions.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/rotor-angle-stability/";
            },},{id: "wiki-secondary-control",
          title: 'Secondary Control',
          description: "Balancing services deployed in the minutes time frame.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/secondary-control/";
            },},{id: "wiki-secondary-reserve",
          title: 'Secondary Reserve',
          description: "Reserve capability within a 10-to-30 minute interval.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/secondary-reserve/";
            },},{id: "wiki-security-constraiend-economic-dispatch",
          title: 'Security Constraiend Economic Dispatch',
          description: "SCED.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/security-constraiend-economic-dispatch/";
            },},{id: "wiki-security-constrained-unit-commitment",
          title: 'Security Constrained Unit Commitment',
          description: "SCUC.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/security-constrained-unit-commitment/";
            },},{id: "wiki-security",
          title: 'Security',
          description: "The degree of risk in a power system&#39;s ability to survive imminent disturbances.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/security/";
            },},{id: "wiki-severity-risk-index",
          title: 'Severity Risk Index',
          description: "SRI. A daily metric that indicates performance of the BES.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/severity-risk-index/";
            },},{id: "wiki-small-signal-stability",
          title: 'Small Signal Stability',
          description: "The ability to maintain synchronism when subjected to small disturbances.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/small-signal-stability/";
            },},{id: "wiki-spinning-reserve",
          title: 'Spinning Reserve',
          description: "A.k.a. Synchronized Reserve. Synchronized generation and ready to serve additional demand.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/spinning-reserve/";
            },},{id: "wiki-spot-market",
          title: 'Spot Market',
          description: "For short-term contractual commitments.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/spot-market/";
            },},{id: "wiki-stability-limit",
          title: 'Stability Limit',
          description: "The maximum power flow possible while maintaining system stability.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/stability-limit/";
            },},{id: "wiki-stability-limits",
          title: 'Stability Limits',
          description: "Stability related transmission limits.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/stability-limits/";
            },},{id: "wiki-stability",
          title: 'Stability',
          description: "The ability to maintain equilibrium during normal and abnormal conditions.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/stability/";
            },},{id: "wiki-storm-resilience-metric",
          title: 'Storm Resilience Metric',
          description: "Focused on the speed of system recovery during storm events.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/storm-resilience-metric/";
            },},{id: "wiki-subregions",
          title: 'Subregions',
          description: "Geographic concepts for emission data by EPA.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/subregions/";
            },},{id: "wiki-subsynchronous-resonance",
          title: 'Subsynchronous Resonance',
          description: "SSR. A condition involving energy exchange at natural frequencies below the synchronous frequency.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/subsynchronous-resonance/";
            },},{id: "wiki-synchronization-process",
          title: 'Synchronization Process',
          description: "The process of the equipment to synchronize its terminal voltage with another voltage source.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/synchronization-process/";
            },},{id: "wiki-synchronization",
          title: 'Synchronization',
          description: "Aligning a device&#39;s terminal voltage with another voltage source.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/synchronization/";
            },},{id: "wiki-synchronized-reserve-service",
          title: 'Synchronized Reserve Service',
          description: "Can be satisfied by online resources in 10 minutes or less.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/synchronized-reserve-service/";
            },},{id: "wiki-synchronous-machine",
          title: 'Synchronous Machine',
          description: "SM. An AC electrical machine operated with a constant electromagnetic field.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/synchronous-machine/";
            },},{id: "wiki-system-flexibility",
          title: 'System Flexibility',
          description: "The ability to respond to system changes and uncertainties.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/system-flexibility/";
            },},{id: "wiki-tertiary-control",
          title: 'Tertiary Control',
          description: "Actions taken to handle current and future contingencies.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/tertiary-control/";
            },},{id: "wiki-thermal-limit-operation-criteria",
          title: 'Thermal Limit Operation Criteria',
          description: "Techniques to control contingency or system violations.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/thermal-limit-operation-criteria/";
            },},{id: "wiki-torsional-resonance",
          title: 'Torsional Resonance',
          description: "The SSR due to torsional interactions between series compensated lines and turbine-generator mechanical shafts.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/torsional-resonance/";
            },},{id: "wiki-transient-stability-assessment",
          title: 'Transient Stability Assessment',
          description: "TSA. Monitor and determine transient stability of the system.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/transient-stability-assessment/";
            },},{id: "wiki-transmission-expansion",
          title: 'Transmission Expansion',
          description: "The addition or modification of facilities of the Transmission System.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/transmission-expansion/";
            },},{id: "wiki-transmission-interconnection-procedures",
          title: 'Transmission Interconnection Procedures',
          description: "TIP.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/transmission-interconnection-procedures/";
            },},{id: "wiki-transmission-planning-horizon",
          title: 'Transmission Planning Horizon',
          description: "Transmission planning period.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/transmission-planning-horizon/";
            },},{id: "wiki-uncertainty",
          title: 'Uncertainty',
          description: "Two types of uncertainty.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/uncertainty/";
            },},{id: "wiki-unit-commitment",
          title: 'Unit Commitment',
          description: "To determine commitment of resources.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/unit-commitment/";
            },},{id: "wiki-vendors",
          title: 'Vendors',
          description: "Power system vendors",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/vendors/";
            },},{id: "wiki-virtual-synchronous-machine",
          title: 'Virtual Synchronous Machine',
          description: "VSM. Equipment that includes a DC/AC converter controlled to mimic a conventional synchronous machine.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/virtual-synchronous-machine/";
            },},{id: "wiki-voltage-dip",
          title: 'Voltage Dip',
          description: "A.k.a. Voltage Sag. Short-duration decreases in RMS voltage",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/voltage-dip/";
            },},{id: "wiki-voltage-limits",
          title: 'Voltage Limits',
          description: "Voltage limits to protect against wide area voltage collapse.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/voltage-limits/";
            },},{id: "wiki-voltage-reductions",
          title: 'Voltage Reductions',
          description: "A.k.a brownouts",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/voltage-reductions/";
            },},{id: "wiki-voltage-stability",
          title: 'Voltage Stability',
          description: "The ability of a power system to maintain steady voltages close to nominal value.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/voltage-stability/";
            },},{id: "wiki-waveform-measurement-unit",
          title: 'Waveform Measurement Unit',
          description: "WMU, a.k.a. synchro-waveform measurement units (SMUs). Sensor device to record synchro-waveforms.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/waveform-measurement-unit/";
            },},{id: "wiki-wholesale-markets",
          title: 'Wholesale Markets',
          description: "The purchase and sale from generators to resellers.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/wholesale-markets/";
            },},{id: "wiki-zonal-price",
          title: 'Zonal Price',
          description: "A pricing mechanism for a specific zone within a control area.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/zonal-price/";
            },},{id: "wiki-zone",
          title: 'Zone',
          description: "",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/zone/";
            },},{id: "wiki-cascading-outage",
          title: 'Cascading Outage',
          description: "A sequence of events in which an initial disturbance triggers dependent component outages.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/cascading-outage/";
            },},{id: "wiki-common-format-for-event-data-exchange",
          title: 'Common Format for Event Data Exchange',
          description: "COMFEDE. Inactive.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/common-format-for-event-data-exchange/";
            },},{id: "wiki-common-format-for-exchange-of-solved-load-flow-data",
          title: 'Common Format for Exchange of Solved Load Flow Data',
          description: "A.k.a. common data format (CDF)",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/common-format-for-exchange-of-solved-load-flow-data/";
            },},{id: "wiki-common-grid-model-exchange-standard",
          title: 'Common Grid Model Exchange Standard',
          description: "CGMES.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/common-grid-model-exchange-standard/";
            },},{id: "wiki-most-severe-single-contingency",
          title: 'Most Severe Single Contingency',
          description: "A single contingency that would result in the greatest loss of resource output.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/most-severe-single-contingency/";
            },},{id: "wiki-dynamic-operating-envelope",
          title: 'Dynamic Operating Envelope',
          description: "DOE. Available capacity to import/export power without violating constraints.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/dynamic-operating-envelope/";
            },},{id: "wiki-operating-envelope",
          title: 'Operating Envelope',
          description: "Allowed power to be transferred to/from the network.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/operating-envelope/";
            },},{id: "wiki-flexibility-options",
          title: 'Flexibility Options',
          description: "Voluntary market products that  manage imbalances across electricity markets.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/flexibility-options/";
            },},{id: "wiki-large-load",
          title: 'Large Load',
          description: "Load facility or aggregation at a single site that can pose reliability risks to the Bulk Power System.",
          section: "Wiki",handler: () => {
              window.location.href = "/wiki/large-load/";
            },},{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:", "_blank");
        },
      },{
        id: 'social-inspire',
        title: 'Inspire HEP',
        section: 'Socials',
        handler: () => {
          window.open("https://inspirehep.net/authors/", "_blank");
        },
      },{
        id: 'social-rss',
        title: 'RSS Feed',
        section: 'Socials',
        handler: () => {
          window.open("/feed.xml", "_blank");
        },
      },{
        id: 'social-scholar',
        title: 'Google Scholar',
        section: 'Socials',
        handler: () => {
          window.open("https://scholar.google.com/citations?user=", "_blank");
        },
      },{
        id: 'social-custom_social',
        title: 'Custom_social',
        section: 'Socials',
        handler: () => {
          window.open("", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
