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
  },{id: "nav-references",
          title: "references",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/references/";
          },
        },{id: "nav-wiki",
          title: "wiki",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/wiki/";
          },
        },{id: "books-the-godfather",
          title: 'The Godfather',
          description: "",
          section: "Books",handler: () => {
              window.location.href = "/books/the_godfather/";
            },},{id: "projects-adequacy",
          title: 'Adequacy',
          description: "The ability to supply the demand and energy requirements of the end-use customers.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/adequacy/";
            },},{id: "projects-ancillary-services",
          title: 'Ancillary Services',
          description: "Services necessary to support the transmission of electric power.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/ancillary-service/";
            },},{id: "projects-area-control-error",
          title: 'Area Control Error',
          description: "ACE. The instantaneous difference between net actual and scheduled interchange.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/area-control-error/";
            },},{id: "projects-area-zone-region",
          title: 'Area, Zone, Region',
          description: "Some geographical concepts in power systems",
          section: "Projects",handler: () => {
              window.location.href = "/projects/area-zone-region/";
            },},{id: "projects-automatic-generation-control",
          title: 'Automatic Generation Control',
          description: "AGC. Automatic regulation of the power output of generators",
          section: "Projects",handler: () => {
              window.location.href = "/projects/automatic-generation-control/";
            },},{id: "projects-balancing-authoritiy",
          title: 'Balancing Authoritiy',
          description: "The responsible entity within a Balancing Authority Area.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/balancing-authority/";
            },},{id: "projects-bilateral-transaction",
          title: 'Bilateral Transaction',
          description: "A direct contract between a seller and buyer outside of a centralized market.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/bilateral-transaction/";
            },},{id: "projects-black-start",
          title: 'black-start',
          description: "Establishing the voltage from around zero",
          section: "Projects",handler: () => {
              window.location.href = "/projects/black-start/";
            },},{id: "projects-bulk-electric-system",
          title: 'Bulk Electric System',
          description: "BES. Transmission Elements and Power resources 100 kV or higher.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/bulk-electric-system/";
            },},{id: "projects-bulk-power-system",
          title: 'Bulk Power System',
          description: "BPS. Facilities and control systems for an transmission network.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/bulk-power-system/";
            },},{id: "projects-capacity-markets",
          title: 'Capacity Markets',
          description: "A market for trading capacity credits.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/capacity-markets/";
            },},{id: "projects-cascading",
          title: 'Cascading',
          description: "The uncontrolled successive loss of System Elements triggered by an incident",
          section: "Projects",handler: () => {
              window.location.href = "/projects/cascading/";
            },},{id: "projects-co-located-load",
          title: 'Co-Located Load',
          description: "Load connected to the an existing or planned facility.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/co-located-load/";
            },},{id: "projects-common-information-model",
          title: 'Common Information Model',
          description: "CIM. A set of open standards for representing power system components",
          section: "Projects",handler: () => {
              window.location.href = "/projects/common-information-model/";
            },},{id: "projects-contingency-reserve",
          title: 'Contingency Reserve',
          description: "Capacity deployed by the Balancing Authority to meet the Disturbance Control Standard.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/contingency-reserve/";
            },},{id: "projects-contingency",
          title: 'Contingency',
          description: "The unexpected failure or outage of a system component.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/contingency/";
            },},{id: "projects-control-performance-standard-1",
          title: 'Control Performance Standard 1',
          description: "CPS1. A standard that measures impact on frequency error",
          section: "Projects",handler: () => {
              window.location.href = "/projects/control-performance-standard-1/";
            },},{id: "projects-control-performance-standard-2",
          title: 'Control Performance Standard 2',
          description: "CPS2. A standard intended to limit unscheduled flows",
          section: "Projects",handler: () => {
              window.location.href = "/projects/control-performance-standard-2/";
            },},{id: "projects-critical-clearing-time",
          title: 'Critical Clearing Time',
          description: "CCT. The maximum permissible duration of the fault.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/critical-clearing-time/";
            },},{id: "projects-critical-inertia",
          title: 'Critical Inertia',
          description: "Minimum level of system inertia necessary to ensure deployment of frequency responsive reserves.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/critical-inertia/";
            },},{id: "projects-day-ahead-markets",
          title: 'Day-ahead Markets',
          description: "Forward markets for electricity to be supplied the following day.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/day-ahead-markets/";
            },},{id: "projects-der",
          title: 'DER',
          description: "Distributed Energy Resources",
          section: "Projects",handler: () => {
              window.location.href = "/projects/distributed-energy-resources/";
            },},{id: "projects-distribution-provider",
          title: 'Distribution Provider',
          description: "Provides and operates the “wires” between the transmission system and the end-use customer.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/distribution-provider/";
            },},{id: "projects-distribution",
          title: 'Distribution',
          description: "The act of distributing gas or electric power to customers.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/distribution/";
            },},{id: "projects-disturbance",
          title: 'Disturbance',
          description: "Any perturbation or sudden loss of generation or interruption of load",
          section: "Projects",handler: () => {
              window.location.href = "/projects/distrubance/";
            },},{id: "projects-economic-dispatch",
          title: 'Economic Dispatch',
          description: "ED. Allocation of generating units for economical production.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/economic-dispatch/";
            },},{id: "projects-electrical-resonance",
          title: 'Electrical Resonance',
          description: "The behavior of power systems with conventional turbine-generators and variable speed induction generators.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/electrical-resonance/";
            },},{id: "projects-equal-area-criterion",
          title: 'Equal Area Criterion',
          description: "EAC and an extended EAC. A method to determine the stability.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/equal-area-criterion/";
            },},{id: "projects-expected-unserved-energy",
          title: 'Expected Unserved Energy',
          description: "EUE. A measure of the capability to continuously serve loads.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/expected-unserved-energy/";
            },},{id: "projects-factors",
          title: 'Factors',
          description: "System sensitivity matrices, such as GSF, PTDF, LODF, BODF, OTDF, etc.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/factors/";
            },},{id: "projects-fast-frequency-response",
          title: 'Fast Frequency Response',
          description: "FFR. Power in response to frequency changes during the arresting phase",
          section: "Projects",handler: () => {
              window.location.href = "/projects/fast-frequency-response/";
            },},{id: "projects-fault",
          title: 'Fault',
          description: "An event such as a short circuit, a broken wire, or an intermittent connection.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/fault/";
            },},{id: "projects-financial-markets",
          title: 'Financial Markets',
          description: "Trading financially settled products.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/financial-markets/";
            },},{id: "projects-financial-transmission-right",
          title: 'Financial Transmission Right',
          description: "FTR. Compensation contract for transmission charges due to grid congestion.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/financial-transmission-right/";
            },},{id: "projects-flexibility",
          title: 'Flexibility',
          description: "The ability to respond to system changes and uncertainties.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/flexibility/";
            },},{id: "projects-flowgate",
          title: 'Flowgate',
          description: "Portion of the transmission system used to analyze power flow impact.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/flowgate/";
            },},{id: "projects-frequency-deviation",
          title: 'Frequency Deviation',
          description: "A change in Interconnection frequency.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/frequency-deviation/";
            },},{id: "projects-frequency-regulation",
          title: 'Frequency Regulation',
          description: "The ability of a Balancing Authority to help maintain Scheduled Frequency.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/frequency-regulation/";
            },},{id: "projects-frequency-response-measure",
          title: 'Frequency Response Measure',
          description: "The median of all Frequency Response observations reported annually.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/frequency-response-measure/";
            },},{id: "projects-frequency-stability",
          title: 'Frequency Stability',
          description: "The ability of a power system to maintain steady frequency following a severe system upset.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/frequency-stability/";
            },},{id: "projects-frequency-response",
          title: 'Frequency Response',
          description: "The ability of a system to react to a change in system frequency.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/frequnecy-response/";
            },},{id: "projects-futures-market",
          title: 'Futures Market',
          description: "For contracts for future delivery of a commodity or security.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/future-markets/";
            },},{id: "projects-horizon",
          title: 'Horizon',
          description: "Time span",
          section: "Projects",handler: () => {
              window.location.href = "/projects/horizon/";
            },},{id: "projects-interchange",
          title: 'Interchange',
          description: "Energy transfers that cross Balancing Authority boundaries.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/interchange/";
            },},{id: "projects-interconnection-reliability-operating-limit",
          title: 'Interconnection Reliability Operating Limit',
          description: "A System Operating Limit that, if violated, could lead to instability or cascading outages.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/interconnection-reliability-operating-limit/";
            },},{id: "projects-interconnection",
          title: 'Interconnection',
          description: "A geographic area where BPS components are synchronized.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/interconnection/";
            },},{id: "projects-interruptible-demand",
          title: 'Interruptible Demand',
          description: "Customer demand that can be interrupted by control or request of the system operator.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/interruptible-demand/";
            },},{id: "projects-ibr",
          title: 'IBR',
          description: "Inverter-based Resources",
          section: "Projects",handler: () => {
              window.location.href = "/projects/inverter-based-resources/";
            },},{id: "projects-localtional-marginal-price",
          title: 'Localtional Marginal Price',
          description: "LMP. Marginal price for energy at the location delivered or received.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/locational-marginal-price/";
            },},{id: "projects-loss-of-load-expectation",
          title: 'Loss-of-Load Expectation',
          description: "LOLE. The number of days per year for which the available generation capacity is insufficient.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/loss-of-load-expectation/";
            },},{id: "projects-loss-of-load-hour",
          title: 'Loss-of-Load Hour',
          description: "LOLH. The number of hours per year where demand will exceed the generating capacity.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/loss-of-load-hour/";
            },},{id: "projects-markets",
          title: 'Markets',
          description: "Some electricity markets in North America",
          section: "Projects",handler: () => {
              window.location.href = "/projects/markets/";
            },},{id: "projects-non-spinning-reserve",
          title: 'Non-Spinning Reserve',
          description: "Unconnected to the system but capable of serving demand within a specified time.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/non-spinning-reserve/";
            },},{id: "projects-operating-reliability",
          title: 'Operating Reliability',
          description: "The ability to withstand sudden disturbances while avoiding uncontrolled cascading blackouts or damage to equipment.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/operating-reliability/";
            },},{id: "projects-operating-reserve-spinning",
          title: 'Operating Reserve – Spinning',
          description: "Generation synchronized to the system and fully available to serve load within the Disturbance Recovery Period.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/operating-reserve-spinning/";
            },},{id: "projects-operating-reserve-supplemental",
          title: 'Operating Reserve – Supplemental',
          description: "Generation or load available to serve load within the Disturbance Recovery Period.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/operating-reserve-supplemental/";
            },},{id: "projects-operating-reserve",
          title: 'Operating Reserve',
          description: "Capability above firm system demand required for regulation, load forecasting error, and outages.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/operating-reserve/";
            },},{id: "projects-oscillation",
          title: 'Oscillation',
          description: "A repetitive motion that can be either undamped, positively damped, or negatively damped.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/oscillation/";
            },},{id: "projects-preface",
          title: 'Preface',
          description: "Disclaimer, acronyms, and change log",
          section: "Projects",handler: () => {
              window.location.href = "/projects/preface/";
            },},{id: "projects-primary-control",
          title: 'Primary Control',
          description: "A.k.a. Frequency Response.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/primary-control/";
            },},{id: "projects-primary-frequency-response",
          title: 'Primary Frequency Response',
          description: "PFR. Immediate proportional response to system Frequency Deviations.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/primary-frequency-response/";
            },},{id: "projects-ramp",
          title: 'Ramp',
          description: "A.k.a. Ramp Rate. The rate at which the interchange schedule or generator output is attained.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/ramp/";
            },},{id: "projects-real-time-reliability-model",
          title: 'Real-Time Reliability Model',
          description: "A computer representation of the power system facilities.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/real-time-reliability-model/";
            },},{id: "projects-regulating-reserve",
          title: 'Regulating Reserve',
          description: "Reserve for AGC to provide normal regulating margin.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/regulating-reserve/";
            },},{id: "projects-reliability",
          title: 'Reliability',
          description: "The probability of satisfactory operation of a power system over the long run.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/reliability/";
            },},{id: "projects-resilience",
          title: 'Resilience',
          description: "Concepts and its metrics.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/resilience/";
            },},{id: "projects-resonance-stability",
          title: 'Resonance Stability',
          description: "The behavior of power systems under oscillatory energy exchange conditions.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/resonance-stability/";
            },},{id: "projects-response-rate",
          title: 'Response Rate',
          description: "The Ramp Rate that a generating unit can achieve under normal conditions.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/response-rate/";
            },},{id: "projects-ride-through",
          title: 'Ride-through',
          description: "Ability to withstand voltage or frequency disturbances and continue operating.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/ride-through/";
            },},{id: "projects-rotating-blackouts",
          title: 'Rotating Blackouts',
          description: "When each set of distribution feeders is interrupted for a limited time and then rotated among individual feeders.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/rotating-blackout/";
            },},{id: "projects-rotor-angle-stability",
          title: 'Rotor Angle Stability',
          description: "The ability to remain in synchronism under normal and disturbed conditions.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/rotor-angle-stability/";
            },},{id: "projects-secondary-control",
          title: 'Secondary Control',
          description: "Balancing services deployed in the “minutes” time frame.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/secondary-control/";
            },},{id: "projects-security",
          title: 'Security',
          description: "The degree of risk in a power system&#39;s ability to survive imminent disturbances.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/security/";
            },},{id: "projects-severity-risk-index",
          title: 'Severity Risk Index',
          description: "SRI. A daily metric that indicates performance of the BES.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/severity-risk-index/";
            },},{id: "projects-small-signal-stability",
          title: 'Small Signal Stability',
          description: "The ability to maintain synchronism when subjected to small disturbances.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/small-signal-stability/";
            },},{id: "projects-spinning-reserve",
          title: 'Spinning Reserve',
          description: "Synchronized generation and ready to serve additional demand.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/spinning-reserve/";
            },},{id: "projects-spot-market",
          title: 'Spot Market',
          description: "For short-term contractual commitments.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/spot-market/";
            },},{id: "projects-stability-limit",
          title: 'Stability Limit',
          description: "The maximum power flow possible while maintaining system stability.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/stability-limit/";
            },},{id: "projects-stability-limits",
          title: 'Stability Limits',
          description: "Limits based on voltage phase angle difference.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/stability-limits/";
            },},{id: "projects-stability",
          title: 'Stability',
          description: "The ability to maintain equilibrium during normal and abnormal conditions.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/stability/";
            },},{id: "projects-subsynchronous-resonance",
          title: 'Subsynchronous Resonance',
          description: "SSR. A condition involving energy exchange at natural frequencies below the synchronous frequency.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/subsynchronous-resonance/";
            },},{id: "projects-synchronization",
          title: 'synchronization',
          description: "Aligning a device&#39;s terminal voltage with another voltage source",
          section: "Projects",handler: () => {
              window.location.href = "/projects/synchronization/";
            },},{id: "projects-synchronous-machine",
          title: 'Synchronous Machine',
          description: "SM. An AC electrical machine operated with a constant electromagnetic field.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/synchronous-machine/";
            },},{id: "projects-tertiary-control",
          title: 'Tertiary Control',
          description: "Actions taken to handle current and future contingencies.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/tertiary-control/";
            },},{id: "projects-thermal-limit-operation-criteria",
          title: 'Thermal Limit Operation Criteria',
          description: "Techniques to control contingency or system violations.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/thermal-limit-operation-criteria/";
            },},{id: "projects-torsional-resonance",
          title: 'Torsional Resonance',
          description: "The SSR due to torsional interactions between series compensated lines and turbine-generator mechanical shafts.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/torsional-resonance/";
            },},{id: "projects-transfer-limits",
          title: 'Transfer Limits',
          description: "Flow limitation across an interface to protect the system from large voltage drops or collapse.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/transfer-limits/";
            },},{id: "projects-transmission-expansion",
          title: 'Transmission Expansion',
          description: "The addition or modification of facilities of the Transmission System.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/transmission-expansion/";
            },},{id: "projects-uncertainty",
          title: 'Uncertainty',
          description: "Two types of uncertainty.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/uncertainty/";
            },},{id: "projects-vendors",
          title: 'Vendors',
          description: "Power system vendors",
          section: "Projects",handler: () => {
              window.location.href = "/projects/vendors/";
            },},{id: "projects-virtual-synchronous-machine",
          title: 'Virtual Synchronous Machine',
          description: "VSM. Equipment that includes a DC/AC converter controlled to mimic a conventional synchronous machine.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/virtual-synchronous-machine/";
            },},{id: "projects-voltage-dip",
          title: 'Voltage Dip',
          description: "Short-duration decreases in RMS voltage.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/voltage-dip/";
            },},{id: "projects-voltage-limits",
          title: 'Voltage Limits',
          description: "Voltage limits to protect against wide area voltage collapse.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/voltage-limits/";
            },},{id: "projects-voltage-reductions",
          title: 'Voltage Reductions',
          description: "A.k.a brownouts",
          section: "Projects",handler: () => {
              window.location.href = "/projects/voltage-reductions/";
            },},{id: "projects-voltage-stability",
          title: 'Voltage Stability',
          description: "The ability of a power system to maintain steady voltages close to nominal value.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/voltage-stability/";
            },},{id: "projects-wholesale-markets",
          title: 'Wholesale Markets',
          description: "The purchase and sale from generators to resellers.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/wholesale-markets/";
            },},{id: "projects-zonal-price",
          title: 'Zonal Price',
          description: "A pricing mechanism for a specific zone within a control area.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/zonal-price/";
            },},{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:%79%6F%75@%65%78%61%6D%70%6C%65.%63%6F%6D", "_blank");
        },
      },{
        id: 'social-inspire',
        title: 'Inspire HEP',
        section: 'Socials',
        handler: () => {
          window.open("https://inspirehep.net/authors/1010907", "_blank");
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
          window.open("https://scholar.google.com/citations?user=qc6CJjYAAAAJ", "_blank");
        },
      },{
        id: 'social-custom_social',
        title: 'Custom_social',
        section: 'Socials',
        handler: () => {
          window.open("https://www.alberteinstein.com/", "_blank");
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
