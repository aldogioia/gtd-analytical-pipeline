# CODEBOOK: METHODOLOGY, INCLUSION CRITERIA, AND VARIABLES

August 2021

---

CONTENTS

INTRODUCTION.....3

THE ORIGINS OF THE GTD ..... 3
Legacy Issues ..... 5
Transparency ..... 5
Inclusiveness ..... 5
Funding ..... 5
Privacy ..... 5
Codebook Changes ..... 7

CURRENT DATA COLLECTION METHODOLOGY (2012-PRESENT) ..... 10
GTD DEFINITION OF TERRORISM AND INCLUSION CRITERIA ..... 11
ADDITIONAL FILTERING MECHANISM: “DOUBT TERRORISM PROPER?” ..... 12
PLOTS, CONSPIRACIES, AND UNSUCCESSFUL ATTACKS ..... 13
SINGLE INCIDENT DETERMINATION ..... 13
CITING THE GLOBAL TERRORISM DATABASE ..... 13

DATABASE VARIABLES.....14

I. GTD ID AND DATE ..... 14
II. INCIDENT INFORMATION ..... 16
III. INCIDENT LOC

---

INTRODUCTION

TM
This document reflects the collection and coding rules for the Global Terrorism Database. The GTD is
an event-level database containing more than 200,000 records of terrorist attacks that took place
around the world since 1970. It is maintained by the National Consortium for the Study of Terrorism
and Responses to Terrorism (START) at the University of Maryland. This codebook describes the GTD’s
methodology, inclusion criteria, and variables. The GTD research team updates the codebook
periodically; key changes are documented below.

This codebook is divided into two broad areas. First, this introduction explains the origins of the GTD,
its data collection methodology and general principles. Our goal is to be as transparent as possible
regarding how the database is produced, with a commitment to creating a highly comprehensive and
consistent terrorist attack dataset. We describe the GTD’s definition of terrorism, inclusion criteria and
other definitional filtering mechanisms, and the current data collection methodology.

Second, the codebook outlines the variables that constitute the GTD and defines the possible values of
the variables. These categories include the GTD ID, incident date, incident location, incident
information, attack information, target/victim information, perpetrator information, perpetrator
statistics, claims of responsibility, weapon information, casualty information, consequences,
kidnapping/hostage taking information, additional information, and source information.

The GTD is publicly available to search, browse, and download on the GTD website. In 2019, the
University of Maryland began a partnership with CHC Global to manage the commercial distribution of
the GTD. All users of the GTD must accept the terms of the End User License Agreement.

Thank you for your interest in the GTD. We hope that you find it to be a useful tool for understanding
the patterns, causes, and consequences of terrorism. If you have any questions or feedback about the
database, please contact the GTD team via email at gtd@start.umd.edu. We welcome your comments
on the data and its application to your work.

The Origins of the GTD

The current GTD is the product of several phases of data collection efforts, each relying on publicly
available, unclassified source materials. These include media articles and electronic news archives, and
to a lesser extent, existing data sets, secondary source materials such as books and journals, and legal
documents.

---

the Study of Violent Groups (ISVG). ISVG continued as the primary collector of data on attacks that
occurred from April 2008 through October 2011. Beginning with cases that occurred in November
2011, all ongoing GTD data collection is conducted by START staff at the University of Maryland.

Table: GTD Data Collection Phases by Collection Institution
Dates of GTD Attacks PGIS CETIS

| Dates of GTD Attacks          | PGIS | CETIS | ISVG | START |
| ----------------------------- | ---- | ----- | ---- | ----- |
| 1/1/1970-12/31/1997           | X    |       |      | X     |
| 1/1/1998-3/31/2008            |      | X     |      | X     |
| 4/1/2008-10/31/2011           |      |       | X    | X     |
| 11/1/2011-06/31/2020(ongoing) |      |       |      | X     |

GTD staff based at START headquarters at the University of Maryland integrated and synthesized data
collected across the entire 1970-2020 time span with the goal of ensuring that the definitions and
methodology are as consistent as possible across all phases of data collection. In addition, GTD staff at
START retroactively coded several key variables not originally available for the PGIS cases, conducted
numerous quality control projects, and supplementaldata collection efforts. These supplemental data
collection efforts involve systematically comparing a variety of additional sources of terrorism incident
data to the GTD to identify any missing events that satisfy GTD inclusion criteria. GTD staff research
these missing events to identify primary sources of information and code theattack details for addition
to the GTD.

Key factors that impact the content of datasets like the GTD include definitions, sources, and
workflows. While the GTD team has applied a single definition of terrorism over the full span of the
database, access to source materials and the efficiency of workflows have varied over time. For
example, the availability of source materials was best at times when the data collection had the
shortest lag behind real time. Improvements in technology and the expansion of the internet have
enhanced both the accessibility of source materials and the efficiency of workflows. In general, users
should interpret trends over time with caution. In particular, note that differences in levels of attacks
and casualties before and after January 1, 1998; April 1, 2008; and January 1, 2012 may be partially
explained by shifts in data collection. Likewise, the GTD is not directly comparable to other sources of
data on terrorism, as differences in definitions, sources, and workflows will produce misleading
inferences.
4

---

Given the varied context of GTD data collection, users of the database should note the following general practices:

**Legacy Issues – The GTD now includes incidents of terrorism from 1970 to June 2020, however a** number of new variables were added to the database beginning with the post-1997 data collection effort. Wherever possible, values for these new variables were retroactively coded for the original incidents, however some of the new variables pertain to details that were not recorded in the first phase of data collection. For any newly added variables that were not retroactively coded and thus only exist for post-1997 cases and earlier events added through recent supplemental collection efforts the Codebook notes the following:

Note: This field is presently only systematically available with incidents occurring after 1997.

## Transparency – The criteria and coding system were designed to be completely transparent and

available to all future users of the database. As such, the commitment was made to describe coding decisions wherever possible.

**Inclusiveness – It was recognized at the outset that researchers and public officials ascribe to varying** definitions of terrorism. Therefore, the approach that was adopted was to collect and structure data such that it would be useful to as broad an audience as possible. The method chosen to achieve this was to err on the side of inclusiveness in our criteria, but to include in the database filtering mechanisms through which users can truncate the data set according to the definition of terrorism that meets their needs. In such scenarios, the user can filter the data according to specific components of established definitions of terrorism. These filtering methods are explored below.

## Funding -- GTD collection, maintenance, and improvements have been supported by:

- United States National Institute of Justice
- United States Department of Homeland Security, Science and Technology Directorate
- United States Department of State, Bureau of Counterterrorism and Countering Violent Extremism
- United States Department of Defense, Combating Terrorism Technical Support Office
- German Federal Foreign Office
- United Kingdom Foreign, Commonwealth, and Development Office _All decisions about GTD data collection are made independently by the research team. The GTD does_ _not represent the official position or policy of any funding agency._ **Privacy – It is the practice of the GTD research team to accurately represent publicly available** information and protect the privacy of individuals. All information in the GTD is drawn from public reporting, and in some cases the database contains information related to specific individuals. This information includes the names of perpetrators, suspected perpetrators, and victims of terrorist attacks as described in source documents. We require that you take every possible precaution to use this information responsibly, for the purpose of advancing the understanding of terrorism.
  GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

Under no circumstances should the GTD be used as an official source of information on the legal disposition of criminal charges, or in support of background investigations on individuals. The GTD is not an official government database. Statistical information contained in the GTD is based on reports from a variety of public media sources that have been vetted for validity and bias. Users should not infer any additional actions or results beyond what is presented in a GTD entry. Users should not infer that an individual associated with a particular attack was tried and convicted of terrorism or any other criminal offense. Users should not assume that a named individual referenced in the GTD is the same person as another who shares the same or similar names. The GTD does not include sufficient unique identifiers or personally identifiable information (PII, e.g., date of birth, home address, identification number) to confirm a particular individual’s identity, and the GTD team does not have access to this information.

While the research team makes every reasonable effort to corroborate facts from multiple independent sources and to eliminate errors through a systematic review process, the magnitude of the database (more than 200,000 attack records) means that occasionally an error will evade detection and appear in the database or a valid incident will not be recorded. In these cases, we value input from users who become aware of such an error to contact us and let us know so we can review the case and make any appropriate corrections. If new documentation about an event becomes available, an entry may be modified, as necessary and appropriate. If you encounter any information that you believe to be inaccurate or incomplete, please contact gtd@start.umd.edu.

The GTD team observes the following general practices to promote accuracy and privacy for publicly reported information related to named individuals.

- Time lag: The GTD is collected on a lag behind real time, helping to avoid erroneous reporting published in the immediate aftermath of an attack, which sometimes includes false identification of alleged assailants. We record information about terrorist attacks that is as “settled” as possible once reporting and investigations have progressed.
- Prioritizing recent sources: The research team prioritizes information from more recently published sources in two ways: 1) in the automatic de-duplication process for source documents the older versions of duplicate documents are discarded and more recent documents—which may contain updated information—are used for data collection; and 2) in the manual data collection process, subject matter experts are trained to critically evaluate the relative accuracy of source documents and prioritize more recent source documents with a higher degree of validity and a lower degree of bias.
- Source validity: The research team reviews and scores the validity each publication in the source document pipeline, and this score is taken into account as appropriate at each stage of the data collection process. Events are not added to the GTD unless they are documented by at least one independent source assessed as highly valid.
- Geo-location: The maximum specificity of geo-location coordinates for the attack is the city centroid, or in the case of large cities, the neighborhood/region centroid.
- Specific language about assailants: Information about named individuals identified as assailants or suspected assailants may be referenced in event summaries. It is the practice of the research team for this information to be as specific as possible. For example, the summary may specify that a named individual “claimed responsibility in a video” or “was charged in connection with the
  GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST attack,” as appropriate based on source documents. If the source documents report conflicting or speculative information about the individuals or groups responsible for the attack, the research team will systematically note that the perpetrator information is “suspected.” If the source documents name individuals only loosely linked to the attack, the research team will not include the names in the summary.

- Victim identification: Including the names of victims of terrorist attacks serves at least two purposes: 1) allowing the data collection team to identify and resolve potential duplicate entries; and 2) helping database users locate particular records in which high-profile individuals were targeted.
- Updating information: The current data collection methodology (described below) supports systematically updating previously recorded events as new information becomes available.

## Codebook Changes – This GTD Codebook supersedes prior codebooks. With only minor exceptions,

however, the user will note that variables and variable values applied in the current GTD are consistent with those used in former versions of the GTD. The following changes have been made to the variables/values:

## No substantive changes were made to the codebook 2019 – 2021.

Changes made in July 2018

- The following changes were made to the target subtype (targsubtype) variables. All changes were applied retroactively to the entire dataset. -Target subtype = 1 was changed from “Gas/Oil” to “Gas/Oil/Electric.” -Target subtype = 65 was changed from “Refugee Camp” to “Refugee (including
  Camps/IDP/Asylum Seekers).” Attacks against these targets were re-classified under target type = 14 (Private Citizens and Property) rather than target type = 13 (Other). -Target subtype = 112 was added to capture attacks targeting “Legal Services.” -Target subtype = 113 was added to capture attacks targeting individuals whom perpetrators identify as “Alleged Informants.”

- Weapon type = 6 (weaptype) was changed from “Explosives/Bombs/Dynamite” to “Explosives” for brevity. This does not represent a substantive change.
- The following changes were made to the weapon subtype (weapsubtype) variables. All changes were applied retroactively to the entire dataset. -Weapon subtype = 2 was changed from “Automatic Weapon (including semiautomatic)” to “Automatic or Semi-Automatic Rifle.” This does not represent a substantive change. -Weapon subtype = 31 was added to capture attacks involving “Pipe Bombs.”

Changes made in June 2017

- A new weapon subtype (weapsubtype) called “Explosive” was created under the weapon type (weaptype) “Chemical” to document chemical weapons that were delivered via explosive device. Users who are interested in comprehensively identifying attacks in which explosive devices were used should consider this classification, as well as any attacks for which any of the _weaptype fields are marked “Explosives/Bombs/Dynamite.”_
  GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

- In previous versions of the GTD attacks carried out by unaffiliated individuals had “Unaffiliated Individual(s)” recorded in the Perpetrator Group Name (gname) field. Noting inconsistency between coding these cases with “Unaffiliated Individual(s)” versus recording available information about the generic identity of the perpetrators, the “Unaffiliated Individual(s)” information has been removed from the gname field and placed in a new variable called “Unaffiliated Individual(s)” (individual). All cases in question were reviewed and, where possible, information about the generic identity of the perpetrators was recorded in the gname field. Coding details for the individual variable can be found below. Likewise, all cases where _gname was recorded as “Other” have been reviewed and re-classified as appropriate._
- Previous versions of the GTD recorded the number of injuries (nwound) that occurred in New York City on September 11, 2001 as blank or “Unknown” due to the difficulty of determining a valid estimate. While this remains challenging, particularly given the serious long-term health impacts of the September 11
  th attacks, nwound now reflects an estimate for the number of people injured, based on a compilation of information from the 9/11 Victim Compensation Fund. While numerous updates are made to casualty information in the GTD each year, this warrants special acknowledgement due to the considerable impact on statistics. Note also that the number of injuries to US citizens (nwoundus) remains unknown.

- Previous versions of the GTD recorded non-integers in the casualty fields in cases where casualty information was aggregated across multiple attacks in source materials. The non- integers resulted from an equal distribution of casualty counts across reported attacks. (See the section on “preservation of statistical accuracy” below). These numbers have been revised so that, even when casualty information is disaggregated and divided across reported attacks, only whole numbers are recorded. GTD analysts use their best judgment when estimating casualty information that has been aggregated in source documents.
  Changes made in June 2016

- Target subtype (targsubtype) changes for attacks against military targets: Four target subtypes (Navy, Air, Coast Guard, and Army) were removed due to underutilization and lack of mutual exclusivity with other target subtypes. These were replaced with the following target subtypes: Military Weaponry, Military Aircraft, Military Maritime, and Non-combatant Personnel. These changes were applied to the entire dataset.
- Weapon subtype (weapsubtype) changes for attacks involving incendiary weapons: The weapon subtype Flamethrower was removed due to underutilization, and replaced with Molotov Cocktail/Petrol Bomb. This change was applied to the entire dataset.
- Edits were made to more than 70 entries in the Perpetrator Group Name (gname) field. These changes were entirely cosmetic, to improve spelling and style consistency. Note that the entry “Individual” was changed to “Unaffiliated Individual(s)” to more accurately reflect its usage.
- Though not a change to the structure of the codebook, users should note that with the June 2016 publication of the GTD, the entire dataset has been geo-coded and includes Latitude and _Longitude (where known) and information on the Specificity of these coordinates._

## Changes made in June 2015

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

- Previous versions of the GTD included “Russia and the Newly Independent States (NIS)” as a region category. This region was removed and the constituent countries were re-classified as Central Asia or Eastern Europe.
- Previous versions of the GTD included Northern Ireland, Corsica, and Puerto Rico as locations distinct from Great Britain, France, and the United States. With respect to the locations of attacks (country), Northern Ireland and Great Britain have been combined and renamed United Kingdom. Corsica has been combined with France. Puerto Rico has been combined with the United States. These changes do not impact the target nationality variables.
- Previous versions of the GTD used the informal names Congo (Kinshasa) and Congo (Brazzaville) to refer to the Democratic Republic of the Congo (formerly Zaire) and the Republic of the Congo (formerly the People’s Republic of the Congo), respectively. The GTD now uses the formal names for these countries as they existed at the time of the attack. These changes impact the country (country) and target nationality (natlty) variables.
  Changes made in August 2014

- Addition of new alternative designation, “State Actor,” for attacks that are classified as “Doubt Terrorism Proper” because it is unclear whether they were carried out by state actors. This category has only been in use for events that occurred after 2012.
- In previous versions of the database the “Doubt Terrorism Proper” variable and “Alternative” categories were only systematically available for attacks that occurred post-1997. We have reviewed the historical data to classify cases as “Doubt Terrorism Proper” or not whenever possible. There remain a large number of historical cases for which this classification is unknown due to insufficient information.
- Addition of Related ID variable, which identifies the eventID numbers of attacks that were carried out as part of a coordinated event.
  Changes made prior to August 2014

- The addition of targetsubtype1, targetsubtype2, and targetsubtype3 for all cases
- The addition of international/domestic variables: INT_LOG, INT_IDEO, INT_MISC, and INT_ANY.
- The addition of latitude and longitude, and geo-coding specificity for a select set of regions.
- The removal of the situation of multi-party conflict and claim of responsibility confirmed variables due to lack of definitional clarity and inconsistent coding.
- Changing alternative designation categories to improve the mutual exclusivity of categories. See below for new values; these changes are reflected in all cases for which this variable was collected.
- Adjustments to weapon subtype categories: -Combined two categories “Knife” and “Sharp Object Other Than Knife” into one
  category “Knives and Other Sharp Objects” -Added two new categories, “Dynamite/TNT” and “Sticky Bomb” under the heading of “Bombs/Dynamite/Explosives”

- The addition of “Unarmed Assault” as a value for the “Attack Type” variable.
- The addition of “Violent Political Parties” as a value for the “Target/Victim Type” variable.
- Due to the rarity of relevant incidents, the removal of “Agriculture” as a value for the “Target/Victim Type” variable. It is now subsumed under appropriate extant values.
  GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

- The coding of incidents that occurred in the West Bank and Gaza Strip as separate from Israel.
- The removal of the “Target/Victim Entity” variables (entity1, entity2, entity3) due to redundancy with “Target/Victim Type” variables (targtype1, targtype2, targtype3).
- The replacement of “Perpetrator Group(s) Suspected/Unconfirmed” (guncertain) with group- specific versions of the same variable (guncertain1, guncertain2, guncertain3).
  These changes have been applied retroactively to all relevant GTD data unless otherwise indicated.

## Current Data Collection Methodology (2012-present)

In order to maximize the efficiency, accuracy, and completeness of GTD collection, the GTD team at START combines automated and manual data collection strategies. The process begins with a universe of over one million media articles on any topic published daily worldwide in order to identify the relatively small subset of articles that describe terrorist attacks. This is accomplished by applying customized keyword filters to the “fire hose” of media articles available through a subscription to the Metabase Application Programming Interface (API) provided by Lexis Nexis. The English-language content from Metabase is supplemented with articles accessed via API from BBC Monitoring, which includes English-language translations of sources from around 150 countries in over 100 languages. (Note: In the past the process included translated content from Open Source Enterprise). This filter isolates an initial pool of potentially relevant articles, approximately 400,000 per month. These articles are then processed using more sophisticated natural language processing (NLP) and machine learning techniques to further refine the results, remove duplicate articles, and identify articles that are likely to be relevant. The GTD team manually reviews this second subset of articles to identify the unique events that satisfy the GTD inclusion criteria and are subsequently researched and coded according to the specifications of the GTD Codebook. Each month, GTD researchers at START review approximately 8,000 - 16,000 articles and identify attacks to be added to the GTD.

The availability of valid source documents cannot be taken for granted and in fact varies considerably, often over time and by location. Because the validity of the data is critically important, the GTD team recognizes this variation and assesses the quality of the sources. Information from high-quality sources—those that are independent (free of influence from the government, political perpetrators, or corporations), those that routinely report externally verifiable content, and those that are primary rather than secondary—is prioritized over information from poor sources. In order for an event to be _recorded in the GTD it must be documented by at least one such high-quality source. Events that are_ only documented by distinctly biased or unreliable sources are not included in the GTD, however the GTD does include certain information from potentially biased sources, such as perpetrator claims of responsibility or details about the motive of the attack. Note that particular scarcity of high-quality sources in certain geographic areas results in conservative documentation of attacks in those areas in the GTD.

The transition to entirely START-based data collection prompted the development of customized document management and data collection tools that streamline the process from beginning to end. The Data Management System (DMS) integrates the tasks of source article management and evaluation, case identification, and case coding into a single online platform. It applies state-of-the-art

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST technologies to each stage of the data collection process, provides staff with a user-friendly interface
tailored for GTD data collection, and supports a specialized coding strategy with several layers of
quality control.

The coding strategy relies on six coding teams that each specialize on a particular domain of the GTD
Codebook. The domains include location, perpetrators, targets, weapons and tactics, casualties and
consequences, and general information. Each team is comprised of three to six undergraduate or
graduate student interns led by a full-time research assistant, and is responsible for coding the domainspecific variables for each event in the GTD. The domain team leader is responsible for training and
supervision of team members, and ensuring the quality of the coded data. This approach guarantees
that each piece of information is coded and reviewed by someone who is closely familiar with the
particular coding guidelines for the domain, as well as the relevant context. For example, the
perpetrator domain team will have greater familiarity with active perpetrator organizations, their
naming conventions, aliases, spelling variations, factions, and splinter organizations, making them wellsuited to systematically record information on the organizations attributed responsibility for an attack.

Although the data collection process developed at the University of Maryland has improved the
internal consistency and comprehensiveness of the GTD, as with any shift in data collection
methodology it is critical to recognize the implications for analysis. The first year of data collected
under the new process, 2012, represents a dramatic increase in the total number of worldwide
terrorist attacks over 2011. Although this increase likely reflects recent patterns of terrorism, it is also
partly a result of the improved efficiency of the data collection process. The use of automated
approaches to document classification allows the GTD team to focus more time reviewing only those
unique source articles that are classified as “relevant” by machine learning algorithms. As a result, the
system has the capacity to include a much broader and deeper pool of media sources from around the
world. It is also worth noting that the continuing rapid growth of the internet and news archives in
particular makes a product like Metabase available to researchers, implicitly improving access to a
greater variety of national and local sources. Despite consistency of the GTD definition of terrorism and
inclusion criteria, this exponential growth of available source materials has allowed for the collection of
more comprehensive data on terrorism than any previous effort. The GTD research team will continue
to evaluate the impact of source availability on trends in the database to better advise users on
important implications for analysis. We also continue to work to supplement the GTD “legacy” data
back to 1970 to further improve its completeness. For more information on the current data collection
methodology and its impact on the GTD, see the START Discussion Point on The Benefits and
Drawbacks of Methodological Advancements in Data Collection and Coding: Insights from the Global
Terrorism Database (GTD).

GTD Definition of Terrorism and Inclusion Criteria

The GTD defines a terrorist attack as the threatened or actual use of illegal force and violence by a nonstate actor to attain a political, economic, religious, or social goal through fear, coercion, or
intimidation. In practice this means in order to consider an incident for inclusion in the GTD, all three of
the following attributes must be present:

---

• The incident must be intentional – the result of a conscious calculation on the part of a
perpetrator.
• The incident must entail some level of violence or immediate threat of violence -including

• The incident must entail some level of violence or immediate threat of violence -including
property violence, as well as violence against people.
• The perpetrators of the incidents must be sub-national actors. The database does not include acts

• The perpetrators of the incidents must be sub-national actors. The database does not include acts
of state terrorism.

In addition, at least two of the following three criteria must be present for an incident to be included in
the GTD:

• Criterion 1: The act must be aimed at attaining a political, economic, religious, or social goal. In
terms of economic goals, the exclusive pursuit of profit does not satisfy this criterion. It must
involve the pursuit of more profound, systemic economic change.

• Criterion 2: There must be evidence of an intention to coerce, intimidate, or convey some other
message to a larger audience (or audiences) than the immediate victims. It is the act taken as a
totality that is considered, irrespective if every individual involved in carrying out the act was aware
of this intention. As long as any of the planners or decision-makers behind the attack intended to
coerce, intimidate or publicize, the intentionality criterion is met.

• Criterion 3: The action must be outside the context of legitimate warfare activities. That is, the
act must be outside the parameters permitted by international humanitarian law, insofar as it
targets non-combatants

Each of these latter three criteria filters can be applied to the database on the GTD website and the full
data file.

The “Doubt Terrorism Proper” field records reservation reported in source materials that the incident
in question is exclusively terrorism. Furthermore, such a determination of doubt is subsequently coded
by GTD analysts as conforming to one of five possible alternative designations: 1) Insurgency/Guerilla
Action; 2) Other Crime Type; 3) Intra/Inter-group conflict; 4) Lack of Intentionality; or 5) State Actor. As
is the case with the criteria filters outlined above, the “Doubt Terrorism Proper” filter is available for
use on the GTD website and in the full data file. Note that the “Doubt Terrorism Proper” determination
was only routinely made for incidents that occurred after 1997 and the “State Actor” was only
routinely made for incidents that occurred after 2012.

Additional Filtering Mechanism: “Doubt Terrorism Proper?”

---

## Plots, Conspiracies, and Unsuccessful Attacks

The GTD does not include plots or conspiracies that are not enacted, or at least attempted. For an event to be included in the GTD, the attackers must be “out the door,” en route to execute the attack. Planning, reconnaissance, and acquiring supplies do not meet this threshold.

The GTD does include attacks that were attempted but ultimately unsuccessful. The circumstances vary depending on tactics (for details see the success variable, below). However, in general if a bomb is planted but fails to detonate; if an arsonist is intercepted by authorities before igniting a fire; or, if an assassin attempts and fails to kill his or her intended target, the attack is considered for inclusion in the GTD, and marked success=0.

## Single Incident Determination

Incidents occurring in both the same geographic and temporal point will be regarded as a single incident, but if either the time of occurrence of incidents or their locations are discontinuous, the events will be regarded as separate incidents. Examples:

- _Four truck bombs explode nearly simultaneously in different parts of a major city. This represents_ four incidents.
- _A bomb goes off, and while police are working on the scene the next day, they are attacked by_ _terrorists with automatic weapons. These are two separate incidents, as they were not continuous,_ given the time lag between the two events.
- _A group of militants shoot and kill five guards at a perimeter checkpoint of a petroleum refinery and_ _then proceeds to set explosives and destroy the refinery. This is one incident since it occurred in a_ single location (the petroleum refinery) and was one continuous event.
- _A group of hijackers diverts a plane to Senegal and, while at an airport in Senegal, shoots two_ _Senegalese policemen. This is one incident, since the hijacking was still in progress at the time of_ the shooting and hence the two events occurred at the same time in the same place. If the information available for a complex event does not specify a time lag between, or the exact locations of, multiple terrorist activities, the event is a single incident. If any discontinuity in time or space is noted, the event is comprised of multiple incidents.

## Citing the Global Terrorism Database

The GTD and the GTD Codebook are available to the public for the purpose of analyzing patterns of terrorism around the world. The recommended citations (adjusting style as needed) are:

START (National Consortium for the Study of Terrorism and Responses to Terrorism). (2021). Global *Terrorism Database (GTD) [Data set]. University of Maryland. [https://www.start.umd.edu/gtd*](https://www.start.umd.edu/gtd*)

START (National Consortium for the Study of Terrorism and Responses to Terrorism). (2021, August). _Global Terrorism Database codebook: Methodology, inclusion criteria, and variables. University of_ Maryland. [https://www.start.umd.edu/gtd/downloads/Codebook.pdf](https://www.start.umd.edu/gtd/downloads/Codebook.pdf)

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

DATABASE VARIABLES

I. GTD ID and Date

GTD ID
(eventid)
Numeric Variable

Incidents from the GTD follow a 12-digit Event ID system.

• First 8 numbers – date recorded “yyyymmdd”.
• Last 4 numbers – sequential case number for the given day (0001, 0002 etc). This is

• Last 4 numbers – sequential case number for the given day (0001, 0002 etc). This is
“0001” unless there is more than one case occurring on the same date.

For example, an incident in the GTD occurring on 25 July 1993 would be numbered as
“199307250001”. An additional GTD case recorded for the same day would be
“199307250002”. The next GTD case recorded for that day would be “199307250003”, etc.

In rare cases, corrections to the date of a GTD attack are made. In order to maintain stable
Event ID numbers, date changes are not reflected in the Event ID.

| Year             |
| ---------------- |
| (iyear)          |
| Numeric Variable |

This field contains the year in which the incident occurred. In the case of incident(s) occurring
over an extended period, the field will record the year when the incident was initiated.

Numeric Variable

This field contains the number of the month in which the incident occurred. In the case of
incident(s) occurring over an extended period, the field will record the month when the
incident was initiated.

GLOBAL TERRORISM DATABASE CODEBOOK

---

## Numeric Variable

This field contains the numeric day of the month on which the incident occurred. In the case of incident(s) occurring over an extended period, the field will record the day when the incident was initiated.

For attacks that took place between 1970 and 2011, if the exact day of the event is unknown, this is recorded as “0.” For attacks that took place after 2011, if the exact day of the event is unknown, this is recorded as the midpoint of the range of possible dates reported in source materials and the full range is recorded in the Approximate Date (approxdate) field below.

Approximate Date _(approxdate)_ _Text Variable_

Whenever the exact date of the incident is not known or remains unclear, this field is used to record the approximate date of the incident.

- If the day of the incident is not known, then the value for “Day” is “0”. For example, if an incident occurred in June 1978 and the exact day is not known, then the value for the “Day” field is “0” and the value for the “Approximate Date” field is “June 1978”.
- If the month is not known, then the value for the “Month” field is “0”. For example, if an incident occurred in the first half of 1978, and the values for the day and the month are not known, then the value for the “Day” and “Month” fields will both be “0” and the value for the “Approximate Date” field is “first half of 1978.”
  Extended Incident? _(extended)_ _Categorical Variable_

1 = "Yes" The duration of an incident extended more than 24 hours. 0 = "No" The duration of an incident extended less than 24 hours.

Date of Extended Incident Resolution _(resolution)_ _Numeric Date Variable_

This field only applies if “Extended Incident?” is “Yes” and records the date in which the incident was resolved (hostages released by perpetrators; hostages killed; successful rescue, etc.)

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

## II. Incident Information

Incident Summary _(summary)_ Text Variable

A brief narrative summary of the incident, noting the “when, where, who, what, how, and why.”

Note: This field is presently only systematically available with incidents occurring after 1997.

Inclusion Criteria _(crit1, crit2, crit3)_ _Categorical Variables_

These variables record which of the inclusion criteria (in addition to the necessary criteria) are met. This allows users to filter out those incidents whose inclusion was based on a criterion which they believe does not constitute terrorism proper. Note that for each of the criteria variables a case is coded as “1” if source information indicates that the criterion is met and “0” if source information indicates that the criterion is not met or that there is no indication that it is met.

Criterion 1: POLITICAL, ECONOMIC, RELIGIOUS, OR SOCIAL GOAL (CRIT1)

The violent act must be aimed at attaining a political, economic, religious, or social goal. This criterion is not satisfied in those cases where the perpetrator(s) acted out of a pure profit motive or from an idiosyncratic personal motive unconnected with broader societal change.

1 = "Yes" The incident meets Criterion 1. 0 = "No" The incident does not meet Criterion 1 or there is no indication that the incident meets Criterion 1.

Criterion 2: INTENTION TO COERCE, INTIMIDATE OR PUBLICIZE TO LARGER AUDIENCE(S) _(CRIT2)_

To satisfy this criterion there must be evidence of an intention to coerce, intimidate, or convey some other message to a larger audience (or audiences) than the immediate victims. Such evidence can include (but is not limited to) the following: pre- or post- attack statements by the perpetrator(s), past behavior by the perpetrators, or the particular nature of the target/victim, weapon, or attack type.

1 = "Yes" The incident meets Criterion 2. 0 = "No" The incident does not meet Criterion 2 or no indication.

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

Criterion 3: OUTSIDE INTERNATIONAL HUMANITARIAN LAW (CRIT3)

The action is outside the context of legitimate warfare activities, insofar as it targets non-combatants (i.e. the act must be outside the parameters permitted by international humanitarian law as reflected in the Additional Protocol to the Geneva Conventions of 12 August 1949 and elsewhere).

1 = "Yes" The incident meets Criterion 3. 0 = "No" The incident does not meet Criterion 3.

Doubt Terrorism Proper? _(doubtterr)_ _Categorical Variable_

In certain cases there may be some uncertainty whether an incident meets all of the criteria for inclusion. In these ambiguous cases, where there is a strong possibility, but not certainty, that an incident represents an act of terrorism, the incident is included in GTD and is coded as “Yes” for this variable.

1 = "Yes" There is doubt as to whether the incident is an act of terrorism. 0 = "No" There is essentially no doubt as to whether the incident is an act of terrorism.

Note: This field is presently only systematically available with incidents occurring after 1997. If

this variable was not included in the data collection process at the time the case was coded, “- 9” is recorded in the database.

Alternative Designation _(alternative; alternative_txt)_ _Categorical Variable_

This variable applies to only those cases coded as “Yes” for “Doubt Terrorism Proper?” (above). This variable identifies the most likely categorization of the incident other than terrorism.

1= Insurgency/Guerilla Action 2= Other Crime Type 3= Inter/Intra-Group Conflict 4= Lack of Intentionality 5= State Actors (systematically coded post-2012)

Note: This field is presently only systematically available with incidents occurring after 1997.

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

Part of Multiple Incident _(multiple)_ _Categorical Variable_

In those cases where several attacks are connected, but where the various actions do not constitute a single incident (either the time of occurrence of incidents or their locations are discontinuous – see Single Incident Determination section above), then “Yes” is selected to denote that the particular attack was part of a “multiple” incident.

1 = "Yes" The attack is part of a multiple incident. 0 = "No" The attack is not part of a multiple incident.

Note: This field is presently only systematically available with incidents occurring after 1997.

Related Incidents _(related)_ _Text Variable_

When an attack is part of a coordinated, multi-part incident the GTD IDs of the related incidents are listed here, separated by commas.

Note: This field is presently only systematically available with incidents occurring after 1997.

## III. Incident Location

Country _(country; country_txt)_ _Categorical Variable_

This field identifies the country or location where the incident occurred. Separatist regions, such as Kashmir, Chechnya, South Ossetia, Transnistria, or Republic of Cabinda, are coded as part of the “home” country.

In the case where the country in which an incident occurred cannot be identified, it is coded as “Unknown.”

Note that the geo-political boundaries of many countries have changed over time. In a number of cases, countries that represented the location of terrorist attacks no longer exist; examples include West Germany, the USSR and Yugoslavia. In these cases the country name for the year the event occurred is recorded. As an example, a 1989 attack in Bonn would be recorded as taking place in West Germany (FRG). An identical attack in 1991 would be recorded as taking place in Germany.

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

BREAKUP OF CZECHOSLOVAKIA:
Czech Republic – independence: 1 January 1993

Czech Republic – independence: 1 January 1993
Slovakia – independence: 1 January 1993

Slovakia – independence: 1 January 1993

BREAKUP OF UNION OF SOVIET SOCIALIST
REPUBLICS (USSR):

REPUBLICS (USSR):
Russian Federation – independence: 24 August 1991

Russian Federation – independence: 24 August 1991
Armenia – independence: 21 September 1991

Armenia – independence: 21 September 1991
Azerbaijan – independence: 30 August 1991

Azerbaijan – independence: 30 August 1991
Belarus – independence: 25 August 1991

Estonia – independence: 17 September 1991
Georgia – independence: 9 April 1991

Georgia – independence: 9 April 1991
Kazakhstan – independence: 16 December 1991

Kazakhstan – independence: 16 December 1991
Kyrgyzstan – independence: 31 August 1991

Kyrgyzstan – independence: 31 August 1991
Latvia – independence: 21 August 1991

USSR terminates: 26 December 1991 – 5 January
1992

Latvia – independence: 21 August 1991
Lithuania – independence: 17 September 1991

Lithuania – independence: 17 September 1991
Moldova – independence: 27 August 1991

BREAKUP OF YUGOSLAVIA:
Bosnia and Herzegovina – independence: 11 April

Tajikistan – independence: 9 September 1991
Turkmenistan – independence: 27 October 1991

Uzbekistan – independence: 1 September 1991

Moldova – independence: 27 August 1991
Tajikistan – independence: 9 September 1991

Ukraine – independence: 24 August 1991
Uzbekistan – independence: 1 September 1991

Croatia – independence: 25 June 1991
Kosovo – UNMIK established: 10 June 1999

Kosovo – UNMIK established: 10 June 1999
Macedonia – independence: 8 September 1991

Yugoslavia becomes Serbia-Montenegro: 4 February
2003
Montenegro – independence: 3 June 2006

Macedonia – independence: 8 September 1991
Yugoslavia becomes Serbia-Montenegro: 4 February

Montenegro – independence: 3 June 2006
Serbia – independence: 3 June 2006

Slovenia – independence: 25 June 1991

BREAKUP OF CZECHOSLOVAKIA:
Czech Republic – independence: 1 January 1993

Czech Republic – independence: 1 January 1993
Slovakia – independence: 1 January 1993

Slovakia – independence: 1 January 1993

OTHER:
Eritrea – independence: 24 May 1993

Eritrea – independence: 24 May 1993
Germany – unification: 3 October 1990

Country (Location) Codes
(Note: These codes are also used for the target/victim nationality fields. Entries marked with an

(Note: These codes are also used for the target/victim nationality fields. Entries marked with an
asterisk (*) only appear as target/victim descriptors in the GTD.

4 = Afghanistan 22 = Belize 41 = Central African Republic
5 = Albania 23 = Benin 42 = Chad
6 = Algeria 24 = Bermuda* 43 = Chile
7 = Andorra 25 = Bhutan 44 = China
8 = Angola 26 = Bolivia 45 = Colombia
10 = Antigua and Barbuda 28 = Bosnia-Herzegovina 46 = Comoros
11 = Argentina 29 = Botswana 47 = Republic of the Congo
12 = Armenia 30 = Brazil 49 = Costa Rica
14 = Australia 31 = Brunei 50 = Croatia
15 = Austria 32 = Bulgaria 51 = Cuba
16 = Azerbaijan 33 = Burkina Faso 53 = Cyprus
17 = Bahamas 34 = Burundi 54 = Czech Republic
18 = Bahrain 35 = Belarus 55 = Denmark
19 = Bangladesh 36 = Cambodia 56 = Djibouti
20 = Barbados 37 = Cameroon 57 = Dominica
21 = Belgium 38 = Canada 58 = Dominican Republic
19

GLOBAL TERRORISM DATABASE CODEBOOK

---

59 = Ecuador 106 = Kuwait 157 = Papua New Guinea
60 = Egypt 107 = Kyrgyzstan 158 = Paraguay
61 = El Salvador 108 = Laos 159 = Peru
62 = Equatorial Guinea 109 = Latvia 160 = Philippines
63 = Eritrea 110 = Lebanon 161 = Poland

63 = Eritrea 110 = Lebanon
64 = Estonia 111 = Lesotho

161 = Poland
162 = Portugal

64 = Estonia 111 = Lesotho 162 = Portugal
65 = Ethiopia 112 = Liberia 163 = Puerto Rico*
66 = Falkland Islands 113 = Libya 164 = Qatar

66 = Falkland Islands 113 = Libya
67 = Fiji 114 = Liechtenstein*

164 = Qatar
114 = Liechtenstein* 166 = Romania

67 = Fiji 114 = Liechtenstein* 166 = Romania
68 = Finland 115 = Lithuania 167 = Russia
69 = France 116 = Luxembourg 168 = Rwanda
70 = French Guiana 117 = Macau 169 = Saba (Netherlands
71 = French Polynesia 118 = Macedonia Antilles)*

71 = French Polynesia 118 = Macedonia
72 = Gabon 119 = Madagascar

118 = Macedonia Antilles)*
119 = Madagascar 173 = Saudi Arabia

72 = Gabon 119 = Madagascar 173 = Saudi Arabia
73 = Gambia 120 = Malawi 174 = Senegal

73 = Gambia 120 = Malawi
74 = Georgia 121 = Malaysia
75 = Germany 122 = Maldives

174 = Senegal
175 = Serbia-Montenegro
176 = Seychelles

75 = Germany 122 = Maldives 176 = Seychelles
76 = Ghana 123 = Mali 177 = Sierra Leone
78 = Greece 124 = Malta 178 = Singapore
79 = Greenland* 125 = Man, Isle of* 179 = Slovak Republic
80 = Grenada 126 = Marshall Islands* 180 = Slovenia

80 = Grenada 126 = Marshall Islands*
81 = Guadeloupe 127 = Martinique
83 = Guatemala 128 = Mauritania
84 = Guinea 129 = Mauritius
85 = Guinea-Bissau 130 = Mexico
86 = Guyana 132 = Moldova
87 = Haiti 134 = Mongolia*
88 = Honduras 136 = Morocco
89 = Hong Kong 137 = Mozambique
90 = Hungary 138 = Myanmar
91 = Iceland 139 = Namibia
92 = India 141 = Nepal
93 = Indonesia 142 = Netherlands
94 = Iran 143 = New Caledonia
95 = Iraq 144 = New Zealand

126 = Marshall Islands* 180 = Slovenia
127 = Martinique 181 = Solomon Islands
128 = Mauritania 182 = Somalia
183 = South Africa
184 = South Korea
185 = Spain
134 = Mongolia* 186 = Sri Lanka
189 = St. Kitts and Nevis
137 = Mozambique 190 = St. Lucia
192 = St. Martin*
195 = Sudan
196 = Suriname
142 = Netherlands 197 = Swaziland
143 = New Caledonia 198 = Sweden
144 = New Zealand 199 = Switzerland

95 = Iraq 144 = New Zealand 199 = Switzerland
96 = Ireland 145 = Nicaragua 200 = Syria
97 = Israel 146 = Niger 201 = Taiwan

97 = Israel 146 = Niger
98 = Italy 147 = Nigeria
99 = Ivory Coast 149 = North Korea
100 = Jamaica 151 = Norway
101 = Japan 152 = Oman*
102 = Jordan 153 = Pakistan
103 = Kazakhstan 155 = West Bank and Gaza Strip
104 = Kenya 156 = Panama

201 = Taiwan
202 = Tajikistan
149 = North Korea 203 = Tanzania
204 = Togo
205 = Thailand
206 = Tonga*
155 = West Bank and Gaza Strip 207 = Trinidad and Tobago
208 = Tunisia

---

209 = Turkey
210 = Turkmenistan
212 = Tuvalu*
213 = Uganda
214 = Ukraine
215 = United Arab Emirates
216 = Great Britain*
217 = United States
218 = Uruguay
219 = Uzbekistan
220 = Vanuatu
221 = Vatican City
222 = Venezuela
223 = Vietnam
225 = Virgin Islands (U.S.)*
226 = Wallis and Futuna
228 = Yemen

229 = Democratic Republic of the 406 = South Yemen
Congo 422 = International
230 = Zambia 428 = South Vietnam
231 = Zimbabwe 499 = East Germany (GDR)
233 = Northern Ireland* 520 = Sinhalese*
215 = United Arab Emirates 235 = Yugoslavia 532 = New Hebrides
236 = Czechoslovakia 603 = United Kingdom
238 = Corsica* 604 = Zaire
334 = Asian* 605 = People's Republic of the
347 = East Timor Congo
349 = Western Sahara 999 = Multinational*
351 = Commonwealth of 1001 = Serbia
Independent States* 1002 = Montenegro
359 = Soviet Union 1003 = Kosovo
362 = West Germany (FRG) 1004 = South Sudan
377 = North Yemen
403 = Rhodesia

Region
(region; region_txt)

This field identifies the region in which the incident occurred. The regions are divided into the
following 12 categories, and dependent on the country coded for the case:

1 = North America
Canada, Mexico, United States

---

6 = South Asia Afghanistan, Bangladesh, Bhutan, India, Maldives, Mauritius, Nepal, Pakistan, Sri Lanka

7 = Central Asia Armenia, Azerbaijan, Georgia, Kazakhstan, Kyrgyzstan, Tajikistan, Turkmenistan, Uzbekistan

8 = Western Europe Andorra, Austria, Belgium, Cyprus, Denmark, Finland, France, Germany, Gibraltar, Greece, Iceland, Ireland, Italy, Luxembourg, Malta, Netherlands, Norway, Portugal, Spain, Sweden, Switzerland, United Kingdom, Vatican City, West Germany (FRG)

9 = Eastern Europe Albania, Belarus, Bosnia-Herzegovina, Bulgaria, Croatia, Czech Republic, Czechoslovakia, East Germany (GDR), Estonia, Hungary, Kosovo, Latvia, Lithuania, Macedonia, Moldova, Montenegro, Poland, Romania, Russia, Serbia, Serbia-Montenegro, Slovak Republic, Slovenia, Soviet Union, Ukraine, Yugoslavia

10 = Middle East & North Africa Algeria, Bahrain, Egypt, Iran, Iraq, Israel, Jordan, Kuwait, Lebanon, Libya, Morocco, North Yemen, Qatar, Saudi Arabia, South Yemen, Syria, Tunisia, Turkey, United Arab Emirates, West Bank and Gaza Strip, Western Sahara, Yemen

11 = Sub-Saharan Africa Angola, Benin, Botswana, Burkina Faso, Burundi, Cameroon, Central African Republic, Chad, Comoros, Democratic Republic of the Congo, Djibouti, Equatorial Guinea, Eritrea, Ethiopia, Gabon, Gambia, Ghana, Guinea, Guinea-Bissau, Ivory Coast, Kenya, Lesotho, Liberia, Madagascar, Malawi, Mali, Mauritania, Mozambique, Namibia, Niger, Nigeria, People's Republic of the Congo, Republic of the Congo, Rhodesia, Rwanda, Senegal, Seychelles, Sierra Leone, Somalia, South Africa, South Sudan, Sudan, Swaziland, Tanzania, Togo, Uganda, Zaire, Zambia, Zimbabwe

12 = Australasia & Oceania Australia, Fiji, French Polynesia, New Caledonia, New Hebrides, New Zealand, Papua New Guinea, Solomon Islands, Vanuatu, Wallis and Futuna

Province / Administrative Region / State _(provstate)_ _Text Variable_

This variable records the name (at the time of event) of the 1 st order subnational administrative region in which the event occurs.

City _(city)_ _Text Variable_

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

This field contains the name of the city, village, or town in which the incident occurred. If the
city, village, or town for an incident is unknown, then this field contains the smallest
administrative area below provstate which can be found for the incident (e.g., district).

(vicinity)
Categorical Variable

Categorical Variable

1 = "Yes" The incident occurred in the immediate vicinity of the city in question.
0 = "No" The incident in the city itself.

Location Details
(location)

(location)
Text Variable

Text Variable

This field is used to specify additional information about the location of the incident.

Numeric Variable

This field records the latitude (based on WGS1984 standards) of the city in which the event
occurred.

Longitude
(longitude)

(longitude)
Numeric Variable

This field identifies the geospatial resolution of the latitude and longitude fields. The most
specific resolution uniformly available throughout the dataset is the center of the city, village,
or town in which the attack occurred. Coordinates with greater resolution, while possible, are
not systematically included in the database.

This field records the longitude (based on WGS1984 standards) of the city in which the event
occurred.

Geocoding Specificity

Categorical Variable

(specificity)
Categorical Variable

---

2 = event occurred in city/village/town and no lat/long could be found, so coordinates are
for centroid of smallest subnational administrative region identified
3 = event did not occur in city/village/town, so coordinates are for centroid of smallest

3 = event did not occur in city/village/town, so coordinates are for centroid of smallest
subnational administrative region identified
nd st
4 = no 2 order or smaller region could be identified, so coordinates are for center of 1

nd st
4 = no 2 order or smaller region could be identified, so coordinates are for center of 1
order administrative region
st
5 = no 1 order administrative region could be identified for the location of the attack, so

2^{\mathrm{n d}}

\ ^{\ {sf T t t}}

st
5 = no 1 order administrative region could be identified for the location of the attack, so
latitude and longitude are unknown

\ ^{\ {s}^{\ t}}

IV. Attack Information

(attacktype1; attacktype1_txt)
Categorical Variable

Categorical Variable

This field captures the general method of attack and often reflects the broad class of tactics
used. It consists of nine categories, which are defined below. Up to three attack types can be
recorded for each incident. Typically, only one attack type is recorded for each incident unless
the attack is comprised of a sequence of events.

When multiple attack types may apply, the most appropriate value is determined based on the
hierarchy below. For example, if an assassination is carried out through the use of an explosive,
the Attack Type is coded as Assassination, not Bombing/Explosion. If an attack involves a
sequence of events, then the first, the second, and the third attack types are coded in the order
of the hierarchy below rather than the order in which they occurred.

1 = ASSASSINATION
An act whose primary objective is to kill one or more specific, prominent individuals.

An act whose primary objective is to kill one or more specific, prominent individuals.
Usually carried out on persons of some note, such as high-ranking military officers,
government officials, celebrities, etc. Not to include attacks on non-specific members of

Attack Type Hierarchy:
Assassination

Assassination
Hijacking

Hijacking
Kidnapping

Kidnapping
Barricade Incident

Barricade Incident
Bombing/Explosion

Unknown

Bombing/Explosion
Armed Assault

Facility/Infrastructure Attack
Unknown

Armed Assault
Unarmed Assault a targeted group. The killing of a police officer would be an armed assault unless there is reason to believe the attackers singled out a particularly prominent officer for assassination.

## 2 = ARMED ASSAULT

An attack whose primary objective is to cause physical harm or death directly to human beings by use of a firearm, incendiary, or sharp instrument (knife, etc.). Not to include attacks involving the use of fists, rocks, sticks, or other handheld (less-than-lethal) weapons. Also includes attacks involving certain classes of explosive devices in addition _to firearms, incendiaries, or sharp instruments. The explosive device subcategories that_ are included in this classification are grenades, projectiles, and unknown or other explosive devices that are thrown.

## 3 = BOMBING/EXPLOSION

An attack where the primary effects are caused by an energetically unstable material undergoing rapid decomposition and releasing a pressure wave that causes physical damage to the surrounding environment. Can include either high or low explosives (including a dirty bomb) but does not include a nuclear explosive device that releases energy from fission and/or fusion, or an incendiary device where decomposition takes place at a much slower rate. If an attack involves certain classes of explosive devices along with firearms, incendiaries, or sharp objects, then the attack is coded as an armed assault only. The explosive device subcategories that are included in this classification are grenades, projectiles, and unknown or other explosive devices that are thrown in which the bombers are also using firearms or incendiary devices.

## 4 = HIJACKING

An act whose primary objective is to take control of a vehicle such as an aircraft, boat, bus, etc. for the purpose of diverting it to an unprogrammed destination, force the release of prisoners, or some other political objective. Obtaining payment of a ransom should not the sole purpose of a Hijacking, but can be one element of the incident so long as additional objectives have also been stated. Hijackings are distinct from Hostage Taking because the target is a vehicle, regardless of whether there are people/passengers in the vehicle.

## 5 = HOSTAGE TAKING (BARRICADE INCIDENT)

An act whose primary objective is to take control of hostages for the purpose of achieving a political objective through concessions or through disruption of normal operations. Such attacks are distinguished from kidnapping since the incident occurs and usually plays out at the target location with little or no intention to hold the hostages for an extended period in a separate clandestine location.

## 6 = HOSTAGE TAKING (KIDNAPPING)

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

An act whose primary objective is to take control of hostages for the purpose of
achieving a political objective through concessions or through disruption of normal
operations. Kidnappings are distinguished from Barricade Incidents (above) in that they
involve moving and holding the hostages in another location.

7 = FACILITY / INFRASTRUCTURE ATTACK
An act, excluding the use of an explosive, whose primary objective is to cause damage to

An act, excluding the use of an explosive, whose primary objective is to cause damage to
a non-human target, such as a building, monument, train, pipeline, etc. Such attacks
include arson and various forms of sabotage (e.g., sabotaging a train track is a
facility/infrastructure attack, even if passengers are killed). Facility/infrastructure
attacks can include acts which aim to harm an installation, yet also cause harm to
people incidentally (e.g. an arson attack primarily aimed at damaging a building, but
causes injuries or fatalities).

8 = UNARMED ASSAULT
An attack whose primary objective is to cause physical harm or death directly to human

An attack whose primary objective is to cause physical harm or death directly to human
beings by any means other than explosive, firearm, incendiary, or sharp instrument
(knife, etc.). Attacks involving chemical, biological or radiological weapons are
considered unarmed assaults.

9 = UNKNOWN
The attack type cannot be determined from the available information.

The attack type cannot be determined from the available information.

Second Attack Type
(attacktype2; attacktype2_txt)

(attacktype2; attacktype2_txt)
Categorical Variable

Categorical Variable

This variable utilizes the hierarchy and attack type definitions listed above.

Success of a terrorist strike is defined according to the tangible effects of the attack. Success is
not judged in terms of the larger goals of the perpetrators. For example, a bomb that exploded
in a building would be counted as a success even if it did not succeed in bringing the building
down or inducing government repression.

Third Attack Type
(attacktype3; attacktype3_txt)

This variable utilizes the hierarchy and attack type definitions listed above

Categorical Variable

(attacktype3; attacktype3_txt)
Categorical Variable

---

The definition of a successful attack depends on the type of attack. Essentially, the key question is whether or not the attack type took place. If a case has multiple attack types, it is successful if any of the attack types are successful, with the exception of assassinations, which are only successful if the intended target is killed.

1 = "Yes" The incident was successful. 0 = "No" The incident was not successful.

**ASSASSINATION** In order for an assassination to be successful, the target of the assassination must be killed. For example, even if an attack kills numerous people but not the target, it is an unsuccessful assassination.

## ARMED ASSAULT

An armed assault is determined to be successful if the assault takes place and if a target is hit (including people and/or property). Unsuccessful armed assaults are those in which the perpetrators attack and do not hit the target. An armed assault is also unsuccessful if the perpetrators are apprehended on their way to commit the assault. To make this determination, however, there must be information to indicate that an actual assault was imminent.

**BOMBING/EXPLOSION** A bombing is successful if the bomb or explosive device detonates. Bombings are considered unsuccessful if they do not detonate. The success or failure of the bombing is not based on whether it hit the intended target.

**HIJACKING** A hijacking is successful if the hijackers assume control of the vehicle at any point, whereas a hijacking is unsuccessful if the hijackers fail to assume control of the vehicle. The success or failure of the hijacking is not based on whether the vehicle reached the intended destination of the hijackers.

## HOSTAGE TAKING (BARRICADE INCIDENT)

A barricade incident is successful if the hostage takers assume control of the individuals at any point, whereas a barricade incident is unsuccessful if the hostage takers fail to assume control of the individuals.

## HOSTAGE TAKING (KIDNAPPING)

A kidnapping is successful if the kidnappers assume control of the individuals at any point, whereas a kidnapping is unsuccessful if the kidnappers fail to assume control of the individuals.

## FACILITY / INFRASTRUCTURE ATTACK

A facility attack is determined to be successful if the facility is damaged. If the facility has not been damaged, then the attack is unsuccessful.

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

## UNARMED ASSAULT

An unarmed assault is determined to be successful there is a victim that who has been injured. Unarmed assaults that are unsuccessful are those in which the perpetrators do not injure anyone. An unarmed assault is also unsuccessful if the perpetrators are apprehended when on their way to commit the assault. To make this determination, however, there must be information to indicate that an assault was imminent.

Suicide Attack _(suicide)_ _Categorical Variable_

This variable is coded “Yes” in those cases where there is evidence that the perpetrator did not intend to escape from the attack alive.

1 = "Yes" The incident was a suicide attack. 0 = "No" There is no indication that the incident was a suicide attack.

## V. Weapon Information

Information on up to four types and sub-types of the weapons used in an attack are recorded for each case, in addition to any information on specific weapon details reported.

Weapon Type _(weaptype1; weaptype1_txt)_ _Categorical Variable_

Up to four weapon types are recorded for each incident. This field records the general type of weapon used in the incident. It consists of the following categories:

## 1 = Biological

A weapon whose components are produced from pathogenic microorganisms or toxic substances of biological origins.

## 2 = Chemical

A weapon produced from toxic chemicals that is contained in a delivery system and dispersed as a liquid, vapor, or aerosol. This category includes chemical weapons delivered via explosive device.

## 3 = Radiological

A weapon whose components are produced from radioactive materials that emit ionizing radiation and can take many forms.

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

## 4 = Nuclear

A weapon which draws its explosive force from fission, fusion, or a combination of these methods.

## 5 = Firearms

A weapon which is capable of firing a projectile using an explosive charge as a propellant.

## 6 = Explosives

A weapon composed of energetically unstable material undergoing rapid decomposition and releasing a pressure wave that causes physical damage to the surrounding environment. Note that chemical weapons delivered via explosive are classified as “Chemical” with weapon subtype “Explosives.”

## 7 = Fake Weapons

A weapon that was claimed by the perpetrator at the time of the incident to be real but was discovered after-the-fact to be non-existent or incapable of producing the desired effects.

## 8 = Incendiary

A weapon that is capable of catching fire, causing fire, or burning readily and produces intensely hot fire when exploded.

## 9 = Melee

A weapon—targeting people rather than property—that does not involve a projectile in which the user and target are in contact with it simultaneously.

## 10 = Vehicle

An automobile that is used in an incident that does not incorporate the use of explosives such as a car bomb or truck bomb.

## 11 = Sabotage Equipment

A weapon that is used in the demolition or destruction of property (e.g., removing bolts from a train tracks).

## 12 = Other

A weapon that has been identified but does not fit into one of the above categories.

## 13 = Unknown

The weapon type cannot be determined from the available information.

## Weapon Sub-type

_(weapsubtype1; weapsubtype1_txt)_

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

## Categorical Variable

This field records a more specific value for most of the Weapon Types identified immediately above.

The corresponding weapon sub-types for each primary weapon type are as follows:

_**Biological**_ [no corresponding weapon sub-types]

_**Chemical**_ 1 = Poisoning 30 = Explosive

_**Radiological**_ [no corresponding weapon sub-types]

_**Nuclear**_ [no corresponding weapon sub-types]

_**Firearms**_ 2 = Automatic or Semi-Automatic Rifle 3 = Handgun 4 = Rifle/Shotgun (non-automatic) 5 = Unknown Gun Type 6 = Other Gun Type

_**Explosives**_ 7 = Grenade (not RPGs) 8 = Landmine 9 = Mail Bomb (letter, package, parcel) 10 = Pressure Trigger 11 = Projectile (e.g., rockets, mortars, RPGs, missiles) 12 = Remote Device (trigger, control, detonate) 13 = Suicide (carried bodily by human being) 14 = Time Fuse 15 = Vehicle 16 = Unknown Explosive Type 17 = Other Explosive Type 28 = Dynamite/TNT 29 = Sticky Bomb 31 = Pipe Bomb

## Fake Weapons

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

## [no corresponding weapon sub-types]

_**Incendiary**_ 18 = Arson/Fire 19 = Molotov Cocktail/Petrol Bomb 20 = Gasoline or Alcohol

_**Melee**_ 21 = Blunt Object 22 = Hands, Feet, Fists 23 = Knife or Other Sharp Object 24 = Rope or Other Strangling Device 26 = Suffocation 27 = Unknown Weapon Type

_**Vehicle**_ [no corresponding weapon sub-types]

## Sabotage Equipment

[no corresponding weapon sub-types]

_**Other**_ [no corresponding weapon sub-types]

_**Unknown**_ [no corresponding weapon sub-types]

Second Weapon Type _(weaptype2; weaptype2_txt)_ _Categorical Variable_

## Conventions follow “Weapon Type” field.

Second Weapon Sub-Type _(weapsubtype2; weapsubtype2_txt)_ _Categorical Variable_

## Conventions follow “Weapon Sub-Type” field.

Third Weapon Type _(weaptype3; weaptype3_txt)_ _Categorical Variable_

## Conventions follow “Weapon Type” field.

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

Third Weapon Sub-Type _(weapsubtype3; weapsubtype3_txt)_ _Categorical Variable_

## Conventions follow “Weapon Sub-Type” field.

Fourth Weapon Type _(weaptype4; weaptype4_txt)_ _Categorical Variable_

## Conventions follow “Weapon Type” field.

Fourth Weapon Sub-Type _(weapsubtype4; weapsubtype4_txt)_ _Categorical Variable_

## Conventions follow “Weapon Sub-Type” field.

Weapon Details _(weapdetail)_ _Text Variable_

This field notes any pertinent information on the type of weapon(s) used in the incident. Such notes could include the novel use or means of concealing a weapon, specific weapon models, interesting details of the weapons’ origins, etc.

## VI. Target/Victim Information

Information on up to three targets/victims is recorded for each incident. The target/victim information fields coded for each of the three targets include type, name of entity, specific target/victim, and nationality of the target/victim. The field contains information on both intended targets and incidental bystanders, and therefore, intentionality should be carefully considered.

Target/Victim Type _(targtype1; targtype1_txt)_ _Categorical Variable_

The target/victim type field captures the general type of target/victim. When a victim is attacked specifically because of his or her relationship to a particular person, such as a prominent figure, the target type reflects that motive. For example, if a family member of a

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST government official is attacked because of his or her relationship to that individual, the type of target is “government.” This variable consists of the following 22 categories:

## 1 = BUSINESS

Businesses are defined as individuals or organizations engaged in commercial or mercantile activity as a means of livelihood. Any attack on a business or private citizens patronizing a business such as a restaurant, gas station, music store, bar, café, etc.

This includes attacks carried out against corporate offices or employees of firms like mining companies, or oil corporations. Furthermore, includes attacks conducted on business people or corporate officers. Included in this value as well are hospitals and chambers of commerce and cooperatives.

Does not include attacks carried out in public or quasi-public areas such as “business district or commercial area”, or generic business-related individuals such as “businessmen” (these attacks are captured under “Private Citizens and Property”, see below.) Also does not include attacks against generic business-related individuals such as “businessmen.” Unless the victims were targeted because of their specific business affiliation, these attacks belong in “Private Citizens and Property.”

## 2 = GOVERNMENT (GENERAL)

Any attack on a government building; government member, former members, including members of political parties in official capacities, their convoys, or events sponsored by political parties; political movements; or a government sponsored institution where the attack is expressly carried out to harm the government.

This value includes attacks on judges, public attorneys (e.g., prosecutors), courts and court systems, politicians, royalty, head of state, government employees (unless police or military), election-related attacks, or intelligence agencies and spies.

This value does not include attacks on political candidates for office or members of political parties that do not hold an elected office (these attacks are captured in “Private Citizens and Property”).

## 3 = POLICE

This value includes attacks on members of the police force or police installations; this includes police boxes, patrols headquarters, academies, cars, checkpoints, etc. Includes attacks against jails or prison facilities, or jail or prison staff or guards.

## 4 = MILITARY

Includes attacks against military units, patrols, barracks, convoys, jeeps, and aircraft. Also includes attacks on recruiting sites, and soldiers engaged in internal policing functions such as at checkpoints and in anti-narcotics activities. This category also includes peacekeeping units that conduct military operations (e.g., AMISOM)

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

Excludes attacks against non-state militias and guerrillas, these types of attacks are coded as “Terrorist/Non-state Militias” see below.

## 5 = ABORTION RELATED

Attacks on abortion clinics, employees, patrons, or security personnel stationed at clinics.

## 6 = AIRPORTS & AIRCRAFT

An attack that was carried out either against an aircraft or against an airport. Attacks against airline employees while on board are also included in this value.

Includes attacks conducted against airport business offices and executives. Military aircraft are not included.

## 7 = GOVERNMENT (DIPLOMATIC)

Attacks carried out against foreign missions, including embassies, consulates, etc.

This value includes cultural centers that have diplomatic functions, and attacks against diplomatic staff and their families (when the relationship is relevant to the motive of the attack) and property. The United Nations is a diplomatic target.

## 8 = EDUCATIONAL INSTITUTION

Attacks against schools, teachers, or guards protecting school sites. Includes attacks against university professors, teaching staff and school buses. Moreover, includes attacks against religious schools in this value.

As noted below in the “Private Citizens and Property” value, the GTD has several attacks against students. If attacks involving students are not expressly against a school, university or other educational institution or are carried out in an educational setting, they are coded as private citizens and property.

Excludes attacks against military schools (attacks on military schools are coded as “Military,” see below).

## 9 = FOOD OR WATER SUPPLY

Attacks on food or water supplies or reserves are included in this value. This generally includes attacks aimed at the infrastructure related to food and water for human consumption.

## 10 = JOURNALISTS & MEDIA

Includes, attacks on reporters, news assistants, photographers, publishers, as well as attacks on media headquarters and offices.

Attacks on transmission facilities such as antennae or transmission towers, or broadcast infrastructure are coded as “Telecommunications,” see below.

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

## 11 = MARITIME (INCLUDES PORTS AND MARITIME FACILITIES)

Includes civilian maritime: attacks against fishing ships, oil tankers, ferries, yachts, etc. (Attacks on fishermen are coded as “Private Citizens and Property,” see below).

## 12 = NGO

Includes attacks on offices and employees of non-governmental organizations (NGOs). NGOs here include large multinational non-governmental organizations such as the Red Cross and Doctors without Borders, as well as domestic organizations.

Does not include labor unions, social clubs, student groups, and other non-NGO (such cases are coded as “Private Citizens and Property”, see below).

## 13= OTHER

This value includes acts of terrorism committed against targets which do not fit into other categories. Some examples include ambulances, firefighters, and international demilitarized zones.

## 14= PRIVATE CITIZENS & PROPERTY

This value includes attacks on individuals, the public in general or attacks in public areas including markets, commercial streets, busy intersections and pedestrian malls.

Also includes ambiguous cases where the target/victim was a named individual, or where the target/victim of an attack could be identified by name, age, occupation, gender or nationality. This value also includes ceremonial events, such as weddings and funerals.

The GTD contains a number of attacks against students. If these attacks are not expressly against a school, university or other educational institution or are not carried out in an educational setting, these attacks are coded using this value. Also, includes incidents involving political supporters as private citizens and property, provided that these supporters are not part of a government-sponsored event. Finally, this value includes police informers.

Does not include attacks causing civilian casualties in businesses such as restaurants, cafes or movie theaters (these categories are coded as “Business” see above).

## 15 = RELIGIOUS FIGURES/INSTITUTIONS

This value includes attacks on religious leaders, (Imams, priests, bishops, etc.), religious institutions (mosques, churches), religious places or objects (shrines, relics, etc.). This value also includes attacks on organizations that are affiliated with religious entities that are not NGOs, businesses or schools.

Attacks on religious pilgrims are considered “Private Citizens and Property;” attacks on missionaries are considered religious figures.

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

16 = TELECOMMUNICATION
This includes attacks on facilities and infrastructure for the transmission of information. More

This includes attacks on facilities and infrastructure for the transmission of information. More
specifically this value includes things like cell phone towers, telephone booths, television
transmitters, radio, and microwave towers.

17 = TERRORISTS/NON-STATE MILITIAS
Terrorists or members of identified terrorist groups within the GTD are included in this value.

Terrorists or members of identified terrorist groups within the GTD are included in this value.
Membership is broadly defined and includes informants for terrorist groups, but excludes
former or surrendered terrorists.

This value also includes cases involving the targeting of militias and guerillas.

18 = TOURISTS
This value includes the targeting of tour buses, tourists, or “tours.” Tourists are persons who

This value includes the targeting of tour buses, tourists, or “tours.” Tourists are persons who
travel primarily for the purposes of leisure or amusement. Government tourist offices are
included in this value.

The attack must clearly target tourists, not just an assault on a business or transportation
system used by tourists. Travel agencies are coded as business targets.

19 = TRANSPORTATION (OTHER THAN AVIATION)
Attacks on public transportation systems are included in this value. This can include efforts to

Attacks on public transportation systems are included in this value. This can include efforts to
assault public buses, minibuses, trains, metro/subways, highways (if the highway itself is the
target of the attack), bridges, roads, etc.

The GTD contains a number of attacks on generic terms such as “cars” or “vehicles.” These
attacks are assumed to be against “Private Citizens and Property” unless shown to be against
public transportation systems. In this regard, buses are assumed to be public transportation
unless otherwise noted.

20 = UNKNOWN
The target type cannot be determined from the available information.

Attacks on officers, employees or facilities of utility companies excluding the type of facilities
above are coded as business.

The target type cannot be determined from the available information.

---

This value pertains to entities that are both political parties (and thus, coded as “government” in this coding scheme) and terrorists. It is operationally defined as groups that engage in electoral politics and appear as “Perpetrators” in the GTD.

## Target/Victim Subtype

(targsubtype1; targsubtype1_txt) _Categorical Variable_

The target subtype variable captures the more specific target category and provides the next level of designation for each target type. If a target subtype is not applicable this variable is left blank.

The subtypes for each target type are as follows:

_**Business**_ 1 = Gas/Oil/Electric 2 = Restaurant/Bar/Café 3 = Bank/Commerce 4 = Multinational Corporation 5 = Industrial/Textiles/Factory 6 = Medical/Pharmaceutical 7 = Retail/Grocery/Bakery (including cell phone shops and generic shops) 8 = Hotel/Resort 9 = Farm/Ranch 10 = Mining 11 = Entertainment/Cultural/Stadium/Casino 12 = Construction 13 = Private Security Company/Firm 112 = Legal Services

## Government (General)

14 = Judges/Attorneys/Courts 15 = Politician or Political Party Movement/Meeting/Rally 16 = Royalty 17 = Head of State 18 = Government Personnel (excluding police, military) 19 = Election-related 20 = Intelligence 21 = Government Buildings/Facility/Office

_**Police**_ 22 = Police Buildings (Headquarters/Stations/School)

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

23 = Police Patrol (including vehicles and convoys) 24 = Police Checkpoint 25 = Police Security Forces/Officers 26 = Prison/Jail

_**Military**_ 27 = Military Barracks/Base/Headquarters/Checkpost 28 = Military Recruiting Station/Academy 29 = Military Unit/Patrol/Convoy 30 = Military Weaponry 31 = Military Aircraft 32 = Military Maritime 33 = Non-combatant Personnel 34 = Military Personnel (soldiers, troops, officers, forces) 35 = Military Transportation/Vehicle (excluding convoys) 36 = Military Checkpoint 37 = North Atlantic Treaty Organization (NATO) Related 39 = Paramilitary

## Abortion Related

40 = Clinics 41 = Personnel

## Airports & Aircraft

42 = Aircraft (not at an airport) 43 = Airline Officer/Personnel 44 = Airport

## Government (Diplomatic)

45 = Diplomatic Personnel (outside of embassy, consulate) 46 = Embassy/Consulate 47 = International Organization (peacekeeper, aid agency, compound)

## Educational Institution

48 = Teacher/Professor/Instructor 49 = School/University/Educational Building 50 = Other Personnel

## Food and Water Supply

51 = Food Supply 52 = Water Supply

## Journalists & Media

53 = Newspaper Journalist/Staff/Facility

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

54 = Radio Journalist/Staff/Facility 55 = Television Journalist/Staff/Facility 56 = Other (including online news agencies)

**Maritime** 57 = Civilian Maritime 58 = Commercial Maritime 59 = Oil Tanker 60 = Port

_**NGO**_ 61 = Domestic NGO 62 = International NGO

_**Other**_ 63 = Ambulance 64 = Fire Fighter/Truck 66 = Demilitarized Zone (including Green Zone)

## Private Citizens & Property

65 = Refugee (including Camps/IDP/Asylum Seekers) 67 = Unnamed Civilian/Unspecified 68 = Named Civilian 69 = Religion Identified 70 = Student 71 = Race/Ethnicity Identified 72 = Farmer 73 = Vehicles/Transportation 74 = Marketplace/Plaza/Square 75 = Village/City/Town/Suburb 76 = House/Apartment/Residence 77 = Laborer (General)/Occupation Identified 78 = Procession/Gathering (funeral, wedding, birthday, religious) 79 = Public Areas (e.g., Public garden, parking lot, garage, beach, public buildings, camps) 80 = Memorial/Cemetery/Monument 81 = Museum/Cultural Center/Cultural House 82 = Labor Union Related 83 = Protester 84 = Political Party Member/Rally 113 = Alleged Informant

## Religious Figures/Institutions

85 = Religious Figure 86 = Place of Worship

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

## 87 = Affiliated Institution

_**Telecommunication**_ 88 = Radio 89 = Television 90 = Telephone/Telegraph 91 = Internet Infrastructure 92 = Multiple Telecommunication Targets

## Terrorist/Non-State Militia

93 = Terrorist Organization 94 = Non-State Militia

_**Tourists**_ 95 = Tourism Travel Agency 96 = Tour Bus/Van/Vehicle 97 = Tourist 98 = Other Facility

_**Transportation**_ 99 = Bus (excluding tourist) 100 = Train/Train Tracks/ Trolley 101 = Bus Station/Stop 102 = Subway 103 = Bridge/Car Tunnel 104 = Highway/Road/Toll/Traffic Signal 105 = Taxi/Rickshaw

_**Unknown**_ [No corresponding target subtypes]

_**Utilities**_ 106 = Gas 107 = Electricity 108 = Oil

## Violent Political Parties

109 = Party Official/Candidate/Other Personnel 110 = Party Office/Facility 111 = Rally

## Name of Entity

_(corp1)_ _Text Variable_

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

This is the name of the corporate entity or government agency that was targeted. If the element targeted is unspecified, “Unknown” is listed. If no specific entity was targeted, “Not Applicable” is recorded.

Specific Target/Victim _(target1)_ _Text Variable_

This is the specific person, building, installation, etc., that was targeted and/or victimized and is a part of the entity named above. (For example, if the U.S. Embassy in Country X was attacked the “Name of Entity” would be “United States Department of State” and the “Specific Target/Victim” would be “United States Embassy”). If names of victims are known, they are listed here preceded by the specific type of target (e.g., civilians, soldiers, officers).

Nationality of Target/Victim _(natlty1; natlty1_txt)_ _Categorical Variable_

This is the nationality of the target that was attacked, and is not necessarily the same as the country in which the incident occurred, although in most cases it is. For hijacking incidents, the nationality of the plane is recorded and not that of the passengers. For numeric nationality codes, please see the country codes in Section III.

Second Target/Victim Type _(targtype2; targtype2_txt)_ _Categorical Variable_

## Conventions follow “Target/Victim Type” field.

Second Target/Victim Subtype _(targsubtype2; targsubtype2_txt)_ _Categorical Variable_

## Conventions follow “Target/Victim Subtype” field.

Name of Second Entity _(corp2)_ _Text Variable_

## Conventions follow “Name of Entity” field.

## Second Specific Target/Victim

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

(target2)
Text Variable

Text Variable

Conventions follow “Specific Target/Victim” field.

Nationality of Second Target/Victim
(natlty2; natlty2_txt)

(natlty2; natlty2_txt)
Categorical Variable

Categorical Variable

Conventions follow “Nationality of Target” field. For numeric nationality codes, please see the
country codes in Section III.

Third Target/Victim Type
(targtype3; targtype3_txt)

(targtype3; targtype3_txt)
Categorical Variable

Categorical Variable

Third Target/Victim Subtype
(targsubtype3; targsubtype3_txt)

(targsubtype3; targsubtype3_txt)
Categorical Variable

Categorical Variable

Conventions follow “Target/Victim Subtype” field.

Name of Third Entity
(corp3)

(corp3)
Text Variable

Text Variable

Conventions follow “Name of Entity” field.

Third Specific Target/Victim
(target3)

(target3)
Text Variable

Conventions follow “Nationality of Target/Victim” field. For numeric nationality codes, please
see the country codes in Section III.

Conventions follow “Specific Target/Victim” field.

Categorical Variable

Text Variable

GLOBAL TERRORISM DATABASE CODEBOOK

---

## VII. Perpetrator Information

Information on up to three perpetrators is recorded for each incident. This includes the perpetrator group name and the perpetrator group sub-name, as well as details about any claims of responsibility for the attack. Note that the perpetrator attributions recorded for each attack reflect what is reported in open-source media accounts, which does not necessarily indicate a legal finding of culpability.

Perpetrator Group Name _(gname)_ _Text Variable_

This field contains the name of the group that carried out the attack. In order to ensure consistency in the usage of group names for the database, the GTD database uses a standardized list of group names that have been established by project staff to serve as a reference for all subsequent entries.

In the event that the name of a formal perpetrator group or organization is not reported in source materials, this field may contain relevant information about the generic identity of the perpetrator(s) (e.g., “Protestant Extremists”). Note that these categories do not represent discrete entities. They are not exhaustive or mutually exclusive (e.g., “student radicals” and “left-wing militants” may describe the same people). They also do not characterize the behavior of an entire population or ideological movement. For many attacks, generic identifiers are the only information available about the perpetrators. Because of this they are included in the database to provide context; however, analysis of generic identifiers should be interpreted with caution.

If no information about the perpetrator group is available, this field is coded as “Unknown.”

Perpetrator Sub-Group Name _(gsubname)_ _Text Variable_

This field contains any additional qualifiers or details about the name of the group that carried out the attack. This includes but is not limited to the name of the specific faction when available.

Second Perpetrator Group Name _(gname2)_ _Text Variable_

This field is used to record the name of the second perpetrator when responsibility for the attack is attributed to more than one perpetrator. Conventions follow “Perpetrator Group” field.

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

Note that multiple perpetrator group attributions do not necessarily indicate that perpetrator groups collaborated to execute an attack. This could represent competing attributions, competing claims of responsibility, competing accusations, or a combination of these. Note the Perpetrator Group Unconfirmed (guncertain) variable below.

Second Perpetrator Sub-Group Name _(gsubname2)_ _Text Variable_

This field is used to record additional qualifiers or details about the second perpetrator group name when responsibility for the attack is attributed to more than one perpetrator. Conventions follow “Perpetrator Sub-Group Name” field.

Third Perpetrator Group Name _(gname3)_ _Text Variable_

This field is used to record the name of the third perpetrator when responsibility for the attack is attributed to more than two perpetrators. Conventions follow “Perpetrator Group” field.

Note that multiple perpetrator group attributions do not necessarily indicate that perpetrator groups collaborated to execute an attack. This could represent competing attributions, competing claims of responsibility, competing accusations, or a combination of these. Note the Perpetrator Group Unconfirmed (guncertain) variable below.

Third Perpetrator Sub-Group Name _(gsubname3)_ _Text Variable_

This field is used to record additional qualifiers of details about the third perpetrator group name when responsibility for the attack is attributed to more than two perpetrators. Conventions follow “Perpetrator Sub-Group Name” field.

First Perpetrator Group Suspected/Unconfirmed? _(guncertain1)_ _Categorical Variable_

This variable indicates whether or not the information reported by sources about the Perpetrator Group Name(s) is based on speculation or dubious claims of responsibility.

1 = "Yes" The perpetrator attribution(s) for the incident are suspected. 0 = "No" The perpetrator attribution(s) for the incident are not suspected.

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

Second Perpetrator Group Suspected/Unconfirmed? _(guncertain2)_ _Categorical Variable_

This variable indicates whether or not the information reported by sources about the Perpetrator Group Name(s) is based on speculation or dubious claims of responsibility.

1 = "Yes" The perpetrator attribution(s) for the incident are suspected. 0 = "No" The perpetrator attribution(s) for the incident are not suspected.

## Conventions follow “First Perpetrator Group Suspected/Unconfirmed?”

Third Perpetrator Group Suspected/Unconfirmed? _(guncertain3)_ _Categorical Variable_

This variable indicates whether or not the information reported by sources about the Perpetrator Group Name(s) is based on speculation or dubious claims of responsibility.

1 = "Yes" The perpetrator attribution(s) for the incident are suspected. 0 = "No" The perpetrator attribution(s) for the incident are not suspected.

## Conventions follow “First Perpetrator Group Suspected/Unconfirmed?”

Unaffiliated Individual(s) (individual) _Categorical Variable_

This variable indicates whether or not the attack was carried out by an individual or several individuals not known to be affiliated with a group or organization. This information should be interpreted with caution, because it is likely that assailants who might be characterized as “unaffiliated individuals” are frequently unidentified.

1 = "Yes" The perpetrator(s) were identified by name (or specific unnamed minors) and not known to be affiliated with a group or organization. 0 = "No" The perpetrator(s) were not identified as unaffiliated individuals (i.e. the perpetrators were either not identified by name, or were known to be affiliated with a group or organization).

Note: This field is presently only systematically available with incidents occurring after 1997.

Number of Perpetrators _(nperps)_ _Numeric Variable_

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

This field indicates the total number of terrorists participating in the incident. (In the instance of multiple perpetrator groups participating in one case, the total number of perpetrators, across groups, is recorded). There are often discrepancies in information on this value.

Where several independent credible sources report different numbers of attackers, the value of this variable reflects the number given by the majority of sources, unless there is reason to do otherwise. Where there is no majority figure among independent sources, the database records the lowest proffered perpetrator figure, unless there is clear reason to do otherwise. In cases where the number of perpetrators is stated vaguely, for example “…at least 11 attackers”, then the lowest possible number is recorded, in this example, “11.” “-99” or “Unknown” appears when the number of perpetrators is not reported.

Number of Perpetrators Captured _(nperpcap)_ _Numeric Variable_

This field records the number of perpetrators taken into custody. “-99” or “Unknown” appears when there is evidence of captured, but the number is not reported.

Divergent reports on the number of perpetrators captured are dealt with in same manner used for the Number of Perpetrators variable described above.

Note: This field is presently only systematically available with incidents occurring after 1997.

Claim of Responsibility? _(claimed)_ _Categorical Variable_

This field is used to indicate whether a group or person(s) claimed responsibility for the attack. If marked “Yes”, it indicates that a person or a group did in fact claim responsibility. When there are multiple perpetrator groups involved, this field refers to the First Perpetrator Group (separate fields for the Second and Third groups follow below).

1 = "Yes" A group or person claimed responsibility for the attack. 0 = "No" No claim of responsibility was made.

Note: This field is presently only systematically available with incidents occurring after 1997.

Mode for Claim of Responsibility _(claimmode; claimmode_txt)_ _Categorical Variable_

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

This records one of 10 modes used by claimants to claim responsibility and might be useful to
verify authenticity, track trends in behavior, etc. If greater detail exists (for instance, a
particularly novel or strange mode is used) this information is captured in the “Additional
Notes” field.

Mode Values:
1 = Letter 6 = Video
2 = Call (post-incident) 7 = Posted to website, blog, social media
3 = Call (pre-incident) 8 = Personal claim
4 = E-mail 9 = Other
5 = Note left at scene 10 = Unknown

Note: This field is presently only systematically available with incidents occurring after 1997.

Competing Claims of Responsibility?
(compclaim)

This field is used to indicate whether more than one group claimed separate responsibility for
the attack. If marked “Yes”, it indicates that the groups entered in conjunction with the case
each claimed responsibility for the attack (i.e., they did not work together, but each
independently tried to claim credit for the attack).

1 = "Yes" There are competing claims of responsibility for the attack.
0 = "No" There are not competing claims of responsibility for the attack.

0 = "No" There are not competing claims of responsibility for the attack.
-9= “Unknown No indication of competing claims.

0=\ 100^{n}

-9= “Unknown No indication of competing claims.
[NULL] Not applicable (e.g., Perpetrator is unknown; only one perpetrator

[NULL] Not applicable (e.g., Perpetrator is unknown; only one perpetrator
reported; or no claim of responsibility reported)

Note: This field is presently only systematically available with incidents occurring after 1997.

Note: This field is presently only systematically available for incidents occurring after 1997.

Second Group Claim of Responsibility?
(claim2)

Mode for Second Group Claim of Responsibility

Categorical Variable

(claim2)
Categorical Variable

(claimmode2)

No claim of responsibility was made.

---

_Categorical Variable_ Conventions follow the “Mode for Claim of Responsibility” field.

Note: This field is presently only systematically available for incidents occurring after 1997.

Third Group Claim of Responsibility? _(claim3)_ _Categorical Variable_ 1 = "Yes" A group or person claimed responsibility for the attack. 0 = "No" No claim of responsibility was made. Conventions follow the “Claim of Responsibility” field.

Note: This field is presently only systematically available with incidents occurring after 1997.

Mode for Third Group Claim of Responsibility _(claimmode3)_ _Categorical Variable_ Conventions follow “Mode for Claim of Responsibility” field.

Note: This field is presently only systematically available with incidents occurring after 1997.

Motive _(motive)_ _Text Variable_ When reports explicitly mention a specific motive for the attack, this motive is recorded in the “Motive” field. This field may also include general information about the political, social, or economic climate at the time of the attack if considered relevant to the motivation underlying the incident.

Note: This field is presently only systematically available with incidents occurring after 1997.

## VIII. Casualties and Consequences

Total Number of Fatalities _(nkill)_ _Numeric Variable_

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

This field stores the number of total confirmed fatalities for the incident. The number includes all victims and attackers who died as a direct result of the incident.

Where there is evidence of fatalities, but a figure is not reported or it is too vague to be of use, this field remains blank. If information is missing regarding the number of victims killed in an attack, but perpetrator fatalities are known, this value will reflect only the number of perpetrators who died as a result of the incident. Likewise, if information on the number of perpetrators killed in an attack is missing, but victim fatalities are known, this field will only report the number of victims killed in the incident.

Where several independent sources report different numbers of casualties, the database will usually reflect the number given by the most recent source. However, the most recent source will not be used if the source itself is of questionable validity or if the source bases its casualty numbers on claims made by a perpetrator group. When there are several “most recent” sources published around the same time, or there are concerns about the validity of a recent source, the majority figure will be used. Where there is no majority figure among independent sources, the database will record the lowest proffered fatality figure, unless that figure comes from a source of questionable validity or there is another compelling reason to do otherwise. Conflicting reports of fatalities will be noted in the “Additional Notes” field.

_**Note: Preservation of Statistical Accuracy**_

When several cases are linked together, sources sometimes provide a cumulative fatality total for all of the events rather than fatality figures for each incident. In such cases, the preservation of statistical accuracy is achieved by distributing fatalities across the linked incidents. It will be noted in the “Additional Notes” field whenever cumulative totals are divided across multiple events. This method for preserving statistical accuracy is also used for calculating the values for the following fields when individual event totals are unknown: “Number of U.S. Fatalities,” “Number of Perpetrator Fatalities,” “Total Number of Injured,” “Number of U.S. Injured,” and “Number of Perpetrators Injured.”

Number of US Fatalities _(nkillus)_ _Numeric Variable_

This field records the number of U.S. citizens who died as a result of the incident, and follows the conventions of “Total Number of Fatalities” described above. Thus, this field records the number of U.S. victims and U.S. perpetrators who died as a result of the attack. The value for this field is not limited to U.S. citizens killed on U.S. soil, but also includes U.S. citizens who died in incidents occurring outside of the U.S.

Number of Perpetrator Fatalities _(nkillter)_ _Numeric Variable_

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

Limited to only perpetrator fatalities, this field follows the conventions of the “Total Number of Fatalities” field described above.

Total Number of Injured _(nwound)_ _Numeric Variable_

This field records the number of confirmed non-fatal injuries to both perpetrators and victims. It follows the conventions of the “Total Number of Fatalities” field described above.

Number of US Injured _(nwoundus)_ _Numeric Variable_

This field records the number of confirmed non-fatal injuries to U.S. citizens, both perpetrators and victims. It follows the conventions of the “Number of U.S. Fatalities” field described above.

Number of Perpetrators Injured _(nwoundte)_ _Numeric Variable_

Conventions follow the “Number of Perpetrator Fatalities” field described above.

Property Damage _(property)_ _Categorical Variable_

“Yes” appears if there is evidence of property damage from the incident.

1 = "Yes" The incident resulted in property damage. 0 = "No" The incident did not result in property damage. -9 = "Unknown" It is unknown if the incident resulted in property damage.

Extent of Property Damage _(propextent; propextent_txt)_ _Categorical Variable_

If “Property Damage?” is “Yes,” then one of the following four categories describes the extent of the property damage:

1 = Catastrophic (likely ≥ $1 billion) 2 = Major (likely ≥ $1 million but < $1 billion) 3 = Minor (likely < $1 million) 4 = Unknown

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

Value of Property Damage (in USD)
(propvalue)

(propvalue)
Numeric Variable

Numeric Variable

If “Property Damage?” is “Yes,” then the exact U.S. dollar amount (at the time of the incident)
of total damages is listed. Where applicable, property values reported in foreign currencies are
converted to U.S. dollars before being entered into the GTD. If no dollar figure is reported, the
field is left blank. That is, a blank field here does not indicate that there was no property
damage but, rather, that no precise estimate of the value was available. The value of damages
only includes direct economic effects of the incident (i.e. cost of buildings, etc.) and not indirect
economic costs (longer term effects on the company, industry, tourism, etc.).

Protocols for recording inconsistent numbers, etc., listed above are followed (see, for example,
“Number of Perpetrators”).

Property Damage Comments
(propcomment)

(propcomment)
Text Variable

Text Variable

If “Property Damage?” is “Yes,” then non-monetary or imprecise measures of damage may be
described in this field. This field is also used to list specific details about the property that was
damaged in an attack, such as the type of vehicle that was destroyed, the areas or parts of a
building that were damaged, or the types of assets that were stolen.

Hostages or Kidnapping Victims
(ishostkid)

(ishostkid)
Categorical Variable

Categorical Variable

This field records whether or not the victims were taken hostage (i.e. held against their will) or
kidnapped (i.e. held against their will and taken to another location) during an incident.

The victims were taken hostage or kidnapped.
The victims were not taken hostage or kidnapped.

This field records the total number of hostages or kidnapping victims. For successful hijackings,
this value will reflect the total number of crew members and passengers aboard the vehicle at
the time of the incident.

The victims were not taken hostage or kidnapped.
It is unknown if the victims were taken hostage or kidnapped.

It is unknown if the victims were taken hostage or kidnapped.

(nhostkid)
Numeric Variable

Numeric Variable

GLOBAL TERRORISM DATABASE CODEBOOK

---

As with other fields, where several independent sources report different numbers of hostages, the GTD reflects the number given by the most recent source, unless there is reason to do otherwise. When there are several most recent sources available, or there are question about the validity of a recent source, the GTD will report the majority figure from a group of independent sources. Where there is no majority figure among independent sources, the database will record the lowest proffered hostage figure, unless there is clear reason to do otherwise.

In cases where the number of hostages or kidnapping victims is stated vaguely, for example, “…at least 11 hostages”, then the lowest possible number will be recorded, in this example “11.” If the number of hostages is unknown or unidentified, this field records “-99” (unknown).

Number of US Hostages / Kidnapping Victims _(nhostkidus)_ _Numeric Variable_

This field reports the number of U.S. citizens that were taken hostage or kidnapped in the incident. Conventions follow the “Total Number of Hostages/ Kidnapping Victims” field described above.

Hours of Kidnapping / Hostage Incident _(nhours)_ _Numeric Variable_

If the “Attack Type” is “Hostage Taking (Kidnapping),” “Hostage Taking (Barricade Incident),” or a successful “Hijacking,” then the duration of the incident is recorded either in this field or in the next field depending on whether the incident lasted a matter of hours or days. If neither hours nor days are known, both fields are coded as “-99” (unknown).

If the incident lasted for less than 24 hours, this field records the approximate number of hours.

If the incident lasted for more than 24 hours (i.e., at least one day), then the approximate number of days is recorded in the next field.

Days of Kidnapping / Hostage Incident _(ndays)_ _Numeric Variable_

If the “Attack Type” is “Hostage Taking (Kidnapping),” “Hostage Taking (Barricade Incident),” or (successful) “Hijacking” and if the duration of the kidnapping / hostage incident last for more than 24 hours, this field records the duration of the incident in days. If information on hours and days is provided, the figure is rounded to the nearest day.

Country That Kidnappers/Hijackers Diverted To

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

(divert)
Text Variable

Text Variable

If the “Attack Type” is “Hostage Taking (Kidnapping)” or “Hijacking” then this field will list the
country that hijackers diverted a vehicle to, or the country that the kidnap victims were moved
to and held. If hijackers did not divert a vehicle to another country, this field is blank. If a vehicle
was diverted to multiple countries, this field will record the first country that the vehicle was
diverted to, and the others will be listed in the “Additional Notes” field.

Country of Kidnapping/Hijacking Resolution
(kidhijcountry)

(kidhijcountry)
Text Variable

Text Variable

If the “Attack Type” is “Hostage Taking (Kidnapping)” or “Hijacking” then this field lists the
country in which the incident was resolved or ended. If the incident was not resolved in another
country, this field is blank. If a vehicle was diverted to more than one country, this field will
record the last country that it was diverted to, and the others will be listed in the “Additional
Notes” field.

Ransom Demanded
(ransom)

Categorical Variable

The incident involved a demand of monetary ransom.
The incident did not involve a demand of monetary ransom.

The incident did not involve a demand of monetary ransom.
It is unknown if the incident involved a demand of monetary

-9 = "Unknown"

Not applicable

Ransom Amount Demanded from US Sources
(ransomamtus)

Total Ransom Amount Demanded
(ransomamt)

If a ransom was demanded, then the amount (in U.S. dollars) is listed in this field. If a ransom
was demanded but the monetary figure is unknown, then this field will report “-99” (unknown).
If there are conflicting reports on the amount of ransom demanded, the majority figure from
independent sources will be used. If no majority exists, the lowest proffered figure will be used,
unless that figure comes from a source of questionable validity or there is another compelling
reason to do otherwise.

(ransomamt)
Numeric Variable

---

If a ransom was demanded from U.S. sources, then the amount (in U.S. dollars) is listed in this field. If a ransom was demanded from U.S. sources but the monetary figure is unknown, then this field will report “-99” (unknown). If there are conflicting reports on the amount of ransom demanded from a U.S. source, the majority figure from independent sources will be used. If no majority exists, the lowest proffered figure will be used, unless there is a reason to do otherwise.

Total Ransom Amount Paid _(ransompaid)_ _Numeric Variable_

If a ransom amount was paid, then the amount (in U.S. dollars) is listed in this field. If a ransom was paid but the monetary figure was unspecified, then this field will report “-99” (unknown). A value of “-99” will also be reported for any case where it is suspected that a ransom was paid, but it has not been confirmed. If there are conflicting reports on the amount of ransom paid, the majority figure from independent sources will be used. If no majority exists, the lowest proffered figure will be used, unless that figure comes from a source of questionable validity or there is another compelling reason to do otherwise.

Ransom Amount Paid by US Sources _(ransompaidus)_ _Numeric Variable_

If a ransom amount was paid by U.S. sources, then this figure is listed in U.S. dollars. If a ransom was paid by U.S. sources but the monetary figure was unspecified, then this field will report “- 99” (unknown). If there are conflicting reports on the amount of ransom paid by a U.S. source, the majority figure from independent sources will be used. If no majority exists, the lowest proffered figure will be used, unless that figure comes from a source of questionable validity or there is another compelling reason to do otherwise.

Ransom Notes _(ransomnote)_ _Text Variable_

This field is used to record any specific details relating to a ransom that are not captured in the other fields. This includes any information about non-money demands made by perpetrators, as well as information on conflicting reports of how much money was demanded and/or paid.

Note: This field is presently only systematically available with incidents occurring after 1997.

Kidnapping/Hostage Outcome _(hostkidoutcome; hostkidoutcome_txt)_ _Categorical Variable_

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

This field captures the eventual fate of hostages and kidnap victims. If the “Attack Type” is “Hostage Taking (Kidnapping),”“Hostage Taking (Barricade Incident),” or a successful “Hijacking,” then this field applies. The seven values for this field are:

1 = Attempted Rescue 2 = Hostage(s) released by perpetrators 3 = Hostage(s) escaped (not during rescue attempt) 4 = Hostage(s) killed (not during rescue attempt) 5 = Successful Rescue 6 = Combination 7 = Unknown

Number Released/Escaped/Rescued _(nreleased)_ _Numeric Variable_

If the “Attack Type” is “Hostage Taking (Kidnapping),” “Hostage Taking (Barricade Incident),” or a successful “Hijacking,” then this field will apply. This field records the number of hostages who survived the incident.

As with the total number of kidnapping victims, where several independent sources report different numbers of hostages, the database will reflect the number given by the most recent source, unless there is reason to do otherwise. If there are several most recent sources available, the majority number form a group of independent sources will be used, unless there is reason to do otherwise. Where there is no majority figure among independent sources, the database will record the lowest proffered hostage released/escaped/rescued figure, unless there is clear reason to do otherwise.

In cases where the number of hostages released/escaped/rescued is stated vaguely, for example “…at least 11 hostages were released”, then the lowest possible number will be recorded, in this example “11.” If the fate of the hostages is unknown, this field will record “-

99.”

## IX. Additional Information and Sources

Additional Notes _(addnotes)_ _Text Variable_

This field is used to capture additional relevant details about the attack. It may include any of the following information:

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

- Additional information that could not be captured in any of the above fields, such as details about hostage conditions or additional countries hijacked vehicles were diverted to.
- Supplemental important information not specific to the particular attack, such as multiple attacks in the same area or by the same perpetrator.
- Uncertainties about the data (such as differing reports of casualty numbers, aggregated casualty numbers split across multiple incidents, or uncertainty about perpetrators responsible).
- Unusual factors, such as a shift in tactics, the reappearance of an organization, the emergence of a new organization, an attack carried out on a historical date, or an escalation of a violent campaign.
- The fate (legal, health, or otherwise) of either victims or perpetrators where this is mentioned in GTD source documents.
- In addition, the instructions for several fields listed above have specific indications for placing additional information in the “Additional Notes” field, as needed: -_Specific Target/Victim_ If the Target/Victim is multiple victims (e.g., in a kidnapping or assassination), up to three names are recorded in the “Specific Target/Victim” field, with remaining names recorded in the “Additional Notes” field. -_Perpetrator Individual(s)’ Name(s)_ Names of individuals identified as planners, bomb-makers, etc., who are indirectly involved in an attack, may recorded in the “Additional Notes” field. -_Mode for Claim of Responsibility_ If greater detail is needed than provided for the “Mode for Claim of Responsibility” field (for instance, a particularly novel or strange mode is used) this information may be captured in the “Additional Notes” field. -_Kidnapping/Hostage Outcome_ If greater detail is available than the Kidnapping/Hostage Outcome field allows, then further details about the fate of hostages/kidnapped may be recorded in the “Additional Notes” field.
- Notes if an attack has been marked as “doubt terrorism proper” and provides explanation of reasons (excluding cases where Alternative Designation = Insurgency).
  Note: This field is presently only systematically available with incidents occurring after 1997.

## International- Logistical

_(INT_LOG)_ _Categorical Variable_

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

This variable is based on a comparison between the nationality of the perpetrator group and the location of the attack. It indicates whether a perpetrator group crossed a border to carry out an attack. Typically the border is a national border, however in cases where perpetrator groups represent non-contiguous contested territory (e.g., Puerto Rico, Corsica, Northern Ireland) or a secure border (e.g., West Bank and Gaza Strip) the nationality of the perpetrator group is coded as the contested territory and attacks against the parent country are coded as logistically international.

1 = "Yes" The attack was logistically international; the nationality of the perpetrator group differs from the location of the attack. If the perpetrator group is multinational, the attack is logistically international if all of the group’s nationalities differ from the location of the attack. 0 = "No" The attack was logistically domestic; the nationality of the perpetrator group is the same as the location of the attack. If the perpetrator group is multinational, the attack is logistically domestic if any of the group’s nationalities is the same as the location of the attack. -9 = "Unknown" It is unknown if the attack was logistically international or domestic; the nationality of the perpetrator group is unknown.

Note: The nationality of the perpetrator group is not included in the GTD, but was collected as

an auxiliary variable for the purpose of coding the international/domestic variables. It is not available for distribution. Also, perpetrator nationality is only identified for groups or organizations, not for individual perpetrators. For cases where the perpetrator group is unidentified, or the attack was carried out by unaffiliated individuals, the nationality of the perpetrator group is unknown.

## International- Ideological

_(INT_IDEO)_ _Categorical Variable_

This variable is based on a comparison between the nationality of the perpetrator group and the nationality of the target(s)/victim(s). It indicates whether a perpetrator group attacked a target of a different nationality. Unlike the logistically international variable, in cases where perpetrator groups represent non-contiguous contested territory (e.g., Puerto Rico, Corsica, Northern Ireland) or a secure border (e.g., West Bank and Gaza Strip) the nationality of the perpetrator group is coded as the parent country and attacks against the parent country are coded as ideologically domestic.

1 = "Yes" The attack was ideologically international; the nationality of the perpetrator group differs from the nationality of the target(s)/victim(s). If the perpetrator group or target is multinational, the attack is ideologically international.

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

0 = "No" The attack was ideologically domestic; any and all nationalities of the perpetrator group are the same as the nationalities of the target(s)/victim(s). -9 = "Unknown" It is unknown if the attack was logistically international or domestic; the nationality of the perpetrator group or the nationality of the target/victim is unknown.

Note: The nationality of the perpetrator group is not included in the GTD, but was collected as

an auxiliary variable for the purpose of coding the international/domestic variables. It is not available for distribution. Also, perpetrator nationality is only identified for groups or organizations, not for individual perpetrators. For cases where the perpetrator group is unidentified, or the attack was carried out by unaffiliated individuals, the nationality of the perpetrator group is unknown.

International- Miscellaneous _(INT_MISC)_ _Categorical Variable_

This variable is based on a comparison between the location of the attack and the nationality of the target(s)/victim(s). It indicates whether a perpetrator group attacked a target of a different nationality. Unlike the logistically international and ideologically international variables, it does not require information about the nationality of the perpetrator group. If an attack is international on this dimension, it is necessarily also either logistically international or _ideologically international, but it is not clear which one. If an attack is domestic on this_ dimension, it may also be logistically international or ideologically international, or domestic on all dimensions.

1 = "Yes" The attack was miscellaneous international; the location of the attack differs from the nationality of the target(s)/victim(s). 0 = "No" The attack was miscellaneous domestic; the location of the attack is the same as the nationalities of the target(s)/victim(s). -9 = "Unknown" It is unknown if the attack was miscellaneous international or domestic; the nationality of target/victim is unknown.

International- Any of the above _(INT_ANY)_ _Categorical Variable_

1 = "Yes" The attack was international on any of the dimensions described above (logistically, ideologically, miscellaneous) 0 = "No" The attack was domestic on all of the dimensions described above (logistically, ideologically, miscellaneous); -9 = "Unknown" It is unknown if the attack was international or domestic; the value for one or more dimensions is unknown.

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

First Source Citation _(scite1)_ _Text Variable_

This field cites the first source that was used to compile information on the specific incident.

Note: This field is presently only systematically available with incidents occurring after 1997.

Second Source Citation _(scite2)_ _Text Variable_

This field cites the second source that was used to compile information on the specific incident.

Note: This field is presently only systematically available with incidents occurring after 1997.

Third Source Citation _(scite3)_ _Text Variable_

This field cites the third source that was used to compile information on the specific incident.

Note: This field is presently only systematically available with incidents occurring after 1997.

Data Collection _(dbsource)_ _Text Variable_

This field identifies the original data collection effort in which each event was recorded. Each value corresponds to a different data collection project or group. The three largest (PGIS, CETIS, and ISVG) correspond to the original collection efforts for GTD1, GTD2, and GTD3, respectively. The additional values correspond to retrospective data collection efforts undertaken by START as part of larger research projects at the center. The originating source in those projects was used to identify cases that were not in the GTD but could be identified in other reputable media sources. These cases were then researched, sourced, and added to the GTD.

GLOBAL TERRORISM DATABASE CODEBOOK ©UNIVERSITY OF MARYLAND AUGUST

---

Appendix I: Data Collection Efforts for the Global Terrorism Database

| Data Collection Effort                   | # of Events | Originating Sources                                                                                                                                                                                                           |
| ---------------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Anti-Abortion Project 2010               | 186         | Cases from the National Abortion Federation and other data sources on anti-abortion attacks in the United States                                                                                                              |
| Armenian Website                         | 40          | Australian Turkish Media Group                                                                                                                                                                                                |
| CAIN                                     | 1588        | Conflict Archive on the Internet for Northern Ireland                                                                                                                                                                         |
| CBRN Global Chronology                   | 46          | Mohtadi, Hamid and Antu Murshid. 2006. A Global Chronology of Incidents of Chemical, Biological, Radioactive, and Nuclear Attacks: 1950-2005. Minneapolis, MN: National Center for Food Protection and Defense.               |
| CETIS                                    | 16156       | Center for Terrorism and Intelligence Studies (1998-2007)                                                                                                                                                                     |
| Disorders and Terrorism Chronology       | 5           | National Advisory Committee on Criminal Justice Standards and Goals, Task Force on Disorders and Terrorism (1976) Report of the Task Force on Disorders and Terrorism. Washington, D.C.: United States Department of Justice. |
| Eco Project 2010                         | 147         | Cases on eco-terrorism within the United States                                                                                                                                                                               |
| Hewitt Project                           | 1005        | Hewitt, Christopher. 2005. Political Violence and Terrorism in Modern America: A Chronology. Praeger Security International: Westport, CT.                                                                                    |
| Hijacking DB                             | 54          | Federal Aviation Administration. 1983. Aircraft Hijackings and Other Criminal Acts Against Civil Aviation Statistical and Narrative Reports. Washington, DC: Office of Civil Aviation Security.                               |
| HSI                                      | 96          | Homeland Security Institute. 2005. Underlying Reasons for Successful &amp; Unsuccessful Terrorist Attacks Against the U.S. Homeland &amp; Selected U.S. Interests Abroad. Washington, D.C.                                    |
| Hyland                                   | 71          | Hyland, Francis P. 1991. Armenian Terrorism: The Past, the Present, the Prospects. Boulder-San Francisco-Oxford: Westview Press.                                                                                              |
| ISVG                                     | 17205       | Institute for the Study of Violent Groups (2008-2011)                                                                                                                                                                         |
| Leuprecht Canadian Data                  | 6           | Data on attacks in Canada provided by Christian Leuprecht, Royal Military College of Canada                                                                                                                                   |
| PGIS                                     | 63733       | Pinkerton Global Intelligence Services (1970-1997)                                                                                                                                                                            |
| Sageman                                  | 3           | Cases from Marc Sageman&#x27;s Book, Understanding Terror Networks                                                                                                                                                            |
| START Primary Collection                 | 101604      | National Consortium for the Study of Terrorism and Responses to Terrorism (November 2011-present)                                                                                                                             |
| State Department 1997 Document           | 28          | United States Department of State. 1997. Significant Incidents of Political Violence Against Americans. Washington, D.C.: Bureau of Diplomatic Security.                                                                      |
| UMD Algeria 2010-2012                    | 847         | Multi-source comparison of events from Algeria between 1990-2010, including Maghreb and Sahel Terrorism by Yonah Alexander.                                                                                                   |
| UMD Assassinations Project               | 18          | Multi-source search of high-profile assassinations                                                                                                                                                                            |
| UMD Black Widows 2011                    | 7           | Multi-source comparison of events by the “Black Widows” attackers in Chechnya.                                                                                                                                                |
| UMD Encyclopedia of World Terrorism 2012 | 48          | Crenshaw, Martha, and John Pimlott (eds.) 2001. Encyclopedia of World Terrorism. Sharpe Reference, Armonk, NY.                                                                                                                |
| UMD JTMM Nepal 2012                      | 104         | Multi-source search of Janatantrik Terai Mukti Morcha and related groups                                                                                                                                                      |
| UMD Miscellaneous                        | 287         | Miscellaneous events from a variety of small data-improvement projects.                                                                                                                                                       |
| UMD Schmid 2012                          | 1164        | Alex P. Schmid, Director of the Terrorism Research Initiative (TRI) provided data he developed in the course of his career in academia and in the United Nations                                                              |
| UMD South Africa                         | 449         | South Africa Truth and Reconciliation Commission of South Africa Report. Johannesburg, South Africa.                                                                                                                          |
| UMD Sri Lanka 2011                       | 404         | Multi-source comparison of events from Sri Lanka between 1970 and 2008                                                                                                                                                        |

---

Appendix II: Country-level statistics for 1993

| Country             | Number of Incidents | Percent | Number Killed | Number Injured | Number US Killed | Number US Injured |
| ------------------- | ------------------- | ------- | ------------- | -------------- | ---------------- | ----------------- |
| Afghanistan         | 20                  | 0.40%   | 65            | 50             | 0                | 1                 |
| Albania             | 2                   | 0.04%   | 0             | 2              | 0                | 0                 |
| Algeria             | 311                 | 6.28%   | 602           | 126            | 0                | 0                 |
| Angola              | 34                  | 0.69%   | 373           | 111            | 0                | 0                 |
| Antigua and Barbuda | 1                   | 0.02%   | 0             | 0              | 0                | 0                 |
| Argentina           | 15                  | 0.30%   | 2             | 1              | 0                | 0                 |
| Armenia             | 6                   | 0.12%   | 5             | 17             | 0                | 0                 |
| Australia           | 2                   | 0.04%   | 0             | 0              | 0                | 0                 |
| Austria             | 9                   | 0.18%   | 0             | 5              | 0                | 0                 |
| Azerbaijan          | 4                   | 0.08%   | 16            | 0              | 0                | 0                 |
| Bangladesh          | 47                  | 0.95%   | 40            | 853            | 0                | 0                 |
| Belarus             | 1                   | 0.02%   | 0             | 0              | 0                | 0                 |
| Belgium             | 4                   | 0.08%   | 2             | 3              | 0                | 0                 |
| Belize              | 1                   | 0.02%   | 0             | 1              | 0                | 1                 |
| Bolivia             | 22                  | 0.44%   | 2             | 1              | 0                | 0                 |
| Bosnia-Herzegovina  | 6                   | 0.12%   | 7             | 8              | 0                | 0                 |
| Brazil              | 24                  | 0.48%   | 97            | 29             | 10               | 0                 |
| Burundi             | 5                   | 0.10%   | 106           | 0              | 0                | 0                 |
| Cambodia            | 216                 | 4.36%   | 279           | 483            | 0                | 1                 |
| Cameroon            | 4                   | 0.08%   | 10            | 2              | 0                | 0                 |
| Canada              | 7                   | 0.14%   | 0             | 0              | 0                | 0                 |
| Chad                | 13                  | 0.26%   | 233           | 276            | 0                | 0                 |
| Chile               | 82                  | 1.66%   | 13            | 31             | 0                | 0                 |
| China               | 21                  | 0.42%   | 7             | 21             | 0                | 0                 |
| Colombia            | 225                 | 4.54%   | 256           | 406            | 0                | 1                 |
| Comoros             | 2                   | 0.04%   | 4             | 0              | 0                | 0                 |
| Congo (Brazzaville) | 23                  | 0.46%   | 106           | 5              | 0                | 0                 |
| Congo (Kinshasa)    | 12                  | 0.24%   | 7             | 20             | 0                | 0                 |
| Corsica             | 67                  | 1.35%   | 1             | 2              | 0                | 0                 |
| Costa Rica          | 3                   | 0.06%   | 0             | 0              | 0                | 0                 |
| Croatia             | 4                   | 0.08%   | 0             | 9              | 0                | 0                 |
| Cuba                | 5                   | 0.10%   | 2             | 0              | 0                | 0                 |
| Cyprus              | 4                   | 0.08%   | 0             | 16             | 0                | 0                 |
| Czech Republic      | 1                   | 0.02%   | 0             | 0              | 0                | 0                 |
| Denmark             | 6                   | 0.12%   | 0             | 36             | 0                | 0                 |
| Djibouti            | 2                   | 0.04%   | 0             | 7              | 0                | 0                 |
| Dominican Republic  | 2                   | 0.04%   | 1             | 0              | 0                | 0                 |

---

|                      | 2   | 0.04% | 0    | 0    | 0   | 0   |
| -------------------- | --- | ----- | ---- | ---- | --- | --- |
| Guadeloupe           | 2   | 0.04% | 0    | 0    | 0   | 0   |
| Guatemala            | 83  | 1.68% | 27   | 9    | 0   | 2   |
| Guinea               | 6   | 0.12% | 12   | 50   | 0   | 0   |
| Guinea-Bissau        | 1   | 0.02% | 1    | 0    | 0   | 0   |
| Haiti                | 67  | 1.35% | 36   | 50   | 0   | 5   |
| Honduras             | 5   | 0.10% | 1    | 4    | 0   | 0   |
| Hong Kong            | 4   | 0.08% | 4    | 5    | 0   | 0   |
| Hungary              | 3   | 0.06% | 0    | 0    | 0   | 0   |
| India                | 249 | 5.03% | 1219 | 2546 | 0   | 0   |
| Indonesia            | 3   | 0.06% | 7    | 1    | 0   | 0   |
| Iran                 | 47  | 0.95% | 78   | 41   | 0   | 0   |
| Iraq                 | 18  | 0.36% | 33   | 59   | 0   | 0   |
| Ireland              | 4   | 0.08% | 1    | 1    | 0   | 0   |
| Israel               | 240 | 4.84% | 142  | 297  | 0   | 0   |
| Italy                | 30  | 0.61% | 14   | 126  | 0   | 1   |
| Jamaica              | 20  | 0.40% | 15   | 17   | 0   | 0   |
| Japan                | 45  | 0.91% | 1    | 1    | 0   | 0   |
| Jordan               | 1   | 0.02% | 1    | 0    | 0   | 0   |
| Kenya                | 25  | 0.50% | 53   | 17   | 0   | 1   |
| Kuwait               | 5   | 0.10% | 1    | 0    | 0   | 0   |
| Laos                 | 1   | 0.02% | 0    | 2    | 0   | 0   |
| Latvia               | 1   | 0.02% | 0    | 0    | 0   | 0   |
| Lebanon              | 64  | 1.29% | 51   | 174  | 0   | 0   |
| Liberia              | 1   | 0.02% | 0    | 1    | 0   | 1   |
| Lithuania            | 3   | 0.06% | 1    | 2    | 0   | 0   |
| Malawi               | 1   | 0.02% | 16   | 0    | 0   | 0   |
| Malaysia             | 2   | 0.04% | 0    | 0    | 0   | 0   |
| Mali                 | 8   | 0.16% | 5    | 0    | 0   | 0   |
| Mauritania           | 1   | 0.02% | 0    | 2    | 0   | 0   |
| Mexico               | 17  | 0.34% | 47   | 22   | 1   | 1   |
| Mozambique           | 8   | 0.16% | 3    | 10   | 0   | 0   |
| Myanmar (Burma)      | 20  | 0.40% | 147  | 70   | 0   | 0   |
| Nepal                | 2   | 0.04% | 0    | 0    | 0   | 0   |
| Netherlands          | 3   | 0.06% | 0    | 0    | 0   | 0   |
| Netherlands Antilles | 2   | 0.04% | 0    | 0    | 0   | 0   |
| New Zealand          | 1   | 0.02% | 0    | 0    | 0   | 0   |
| Nicaragua            | 53  | 1.07% | 87   | 125  | 0   | 2   |
| Niger                | 7   | 0.14% | 5    | 0    | 0   | 0   |

---

| Russia              | 32   | 0.65%   | 203   | 841   | 1   | 5    |
| ------------------- | ---- | ------- | ----- | ----- | --- | ---- |
| Rwanda              | 13   | 0.26%   | 81    | 155   | 0   | 0    |
| Senegal             | 6    | 0.12%   | 121   | 0     | 0   | 0    |
| Sierra Leone        | 4    | 0.08%   | 30    | 9     | 0   | 0    |
| Singapore           | 1    | 0.02%   | 0     | 1     | 0   | 0    |
| Somalia             | 74   | 1.49%   | 115   | 293   | 28  | 124  |
| South Africa        | 426  | 8.60%   | 1009  | 631   | 1   | 0    |
| South Korea         | 4    | 0.08%   | 0     | 1     | 0   | 0    |
| Spain               | 50   | 1.01%   | 19    | 37    | 0   | 0    |
| Sri Lanka           | 29   | 0.59%   | 1268  | 380   | 0   | 0    |
| Sudan               | 2    | 0.04%   | 0     | 0     | 0   | 0    |
| Suriname            | 4    | 0.08%   | 0     | 2     | 0   | 0    |
| Swaziland           | 1    | 0.02%   | 0     | 1     | 0   | 0    |
| Sweden              | 5    | 0.10%   | 0     | 1     | 0   | 0    |
| Switzerland         | 12   | 0.24%   | 2     | 9     | 0   | 0    |
| Taiwan              | 5    | 0.10%   | 34    | 57    | 0   | 0    |
| Tajikistan          | 14   | 0.28%   | 373   | 19    | 0   | 0    |
| Tanzania            | 6    | 0.12%   | 0     | 1     | 0   | 1    |
| Thailand            | 67   | 1.35%   | 34    | 97    | 0   | 0    |
| Togo                | 13   | 0.26%   | 1     | 11    | 0   | 0    |
| Trinidad and Tobago | 2    | 0.04%   | 0     | 0     | 0   | 0    |
| Turkey              | 386  | 7.79%   | 1166  | 403   | 0   | 0    |
| Uganda              | 4    | 0.08%   | 2     | 1     | 0   | 0    |
| United Kingdom      | 59   | 1.19%   | 3     | 133   | 0   | 0    |
| United States       | 28   | 0.57%   | 21    | 1066  | 0   | 1048 |
| Uruguay             | 4    | 0.08%   | 1     | 0     | 0   | 0    |
| Venezuela           | 49   | 0.99%   | 2     | 13    | 0   | 0    |
| Vietnam             | 2    | 0.04%   | 0     | 1     | 0   | 0    |
| Yemen               | 23   | 0.46%   | 12    | 7     | 0   | 2    |
| Yugoslavia          | 5    | 0.10%   | 1     | 5     | 0   | 0    |
| Zambia              | 1    | 0.02%   | 0     | 0     | 0   | 0    |
|                     |      |         |       |       |     |      |
| TOTAL               | 4954 | 100.00% | 10162 | 12176 | 45  | 1214 |
