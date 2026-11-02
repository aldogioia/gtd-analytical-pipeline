import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const workspace = fileURLToPath(new URL('..', import.meta.url));
const sourcePath = path.join(workspace, 'tableau', 'GTD.twb');
const outputPath = path.join(workspace, 'output', 'tableau', 'Visualization revised.twb');

let xml = (await fs.readFile(sourcePath, 'utf8')).replace(/\r\n/g, '\n');

function replaceRequired(search, replacement, label, minimum = 1) {
  const count = xml.split(search).length - 1;
  if (count < minimum) {
    throw new Error(`${label}: expected at least ${minimum} occurrence(s), found ${count}`);
  }
  xml = xml.split(search).join(replacement);
}

function replaceRegexRequired(regex, replacement, label, minimum = 1) {
  let count = 0;
  xml = xml.replace(regex, (...args) => {
    count += 1;
    return typeof replacement === 'function' ? replacement(...args) : replacement;
  });
  if (count < minimum) {
    throw new Error(`${label}: expected at least ${minimum} occurrence(s), found ${count}`);
  }
}

function rewriteDashboard(name, nextName, transform) {
  const startToken = `<dashboard enable-sort-zone-taborder='true' name='${name}'>`;
  const start = xml.indexOf(startToken);
  if (start < 0) throw new Error(`Dashboard not found: ${name}`);
  const end = nextName
    ? xml.indexOf(`<dashboard enable-sort-zone-taborder='true' name='${nextName}'>`, start)
    : xml.indexOf('  </dashboards>', start);
  if (end < 0) throw new Error(`Dashboard end not found: ${name}`);
  const original = xml.slice(start, end);
  const revised = transform(original);
  xml = xml.slice(0, start) + revised + xml.slice(end);
}

function removeZonesByParam(block, params) {
  for (const param of params) {
    const escaped = param.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    block = block.replace(
      new RegExp(`\\n\\s*<zone(?=[^>]*param='${escaped}')[^>]*>[\\s\\S]*?<\\/zone>`, 'g'),
      '',
    );
  }
  return block;
}

// Italian display names. Internal field names and source member values remain unchanged.
const captions = new Map([
  ['Decade', 'Decennio'],
  ['Region Name', 'Regione'],
  ['Country Name', 'Paese'],
  ['Attack Name', 'Tipo di attacco'],
  ['Attack Macro', 'Macro-attacco'],
  ['Target Macro', 'Macro-bersaglio'],
  ['Target Name', 'Bersaglio'],
  ['Weapon Macro', 'Macro-arma'],
  ['Weapon Name', 'Arma'],
  ['Terrorist Group', 'Gruppo responsabile'],
  ['Date Accuracy', 'Precisione della data'],
  ['Nkill Source', 'Fonte dei decessi'],
  ['Nwound Source', 'Fonte dei feriti'],
  ['Is Suicide', 'Attacco suicida'],
  ['Full Date', "Data dell'evento"],
]);
for (const [from, to] of captions) {
  replaceRequired(
    `caption='${from}'`,
    `caption='${to.replaceAll("'", '&apos;')}'`,
    `caption ${from}`,
  );
}

// Percentage formats for proportions and robustness deltas.
for (const caption of [
  'Quota transnazionale',
  'Tasso di successo',
  'Quota vittime stimate',
  'Quota suicidi',
  'Quota ignoti',
  'Scarto',
]) {
  const re = new RegExp(`caption='${caption}' datatype='real' default-format='[^']*'`, 'g');
  if (re.test(xml)) {
    re.lastIndex = 0;
    replaceRegexRequired(
      re,
      `caption='${caption}' datatype='real' default-format='p0.0%'`,
      `format ${caption}`,
    );
  } else {
    replaceRequired(
      `caption='${caption}' datatype='real'`,
      `caption='${caption}' datatype='real' default-format='p0.0%'`,
      `format ${caption}`,
    );
  }
}

// Semantic palette: frequency blue-grey, fatalities red, observed blue, imputed ochre, missing grey.
replaceRequired(
  `<map to='#bab0ac'>\n              <bucket>&quot;[federated.1uwnzur0evf63z12rs1zj14huhen].[ctd:eventid:qk]&quot;</bucket>`,
  `<map to='#4e79a7'>\n              <bucket>&quot;[federated.1uwnzur0evf63z12rs1zj14huhen].[ctd:eventid:qk]&quot;</bucket>`,
  'event count colour',
);
replaceRequired(
  `<map to='#f28e2b'>\n              <bucket>&quot;[federated.1uwnzur0evf63z12rs1zj14huhen].[usr:Calculation_4321186351734784:qk]&quot;</bucket>`,
  `<map to='#e15759'>\n              <bucket>&quot;[federated.1uwnzur0evf63z12rs1zj14huhen].[usr:Calculation_4321186351734784:qk]&quot;</bucket>`,
  'lethality colour',
);
replaceRequired(
  `<encoding attr='color' field='[none:nkill_source:nk]' type='palette'>\n            <map to='#4e79a7'>\n              <bucket>&quot;Imputed&quot;</bucket>\n            </map>\n            <map to='#f28e2b'>\n              <bucket>&quot;Reported&quot;</bucket>`,
  `<encoding attr='color' field='[none:nkill_source:nk]' type='palette'>\n            <map to='#d99000'>\n              <bucket>&quot;Imputed&quot;</bucket>\n            </map>\n            <map to='#4e79a7'>\n              <bucket>&quot;Reported&quot;</bucket>`,
  'death source palette',
);
replaceRequired(
  `<encoding attr='color' field='[none:nwound_source:nk]' type='palette'>\n            <map to='#4e79a7'>\n              <bucket>&quot;Not Reported&quot;</bucket>\n            </map>\n            <map to='#f28e2b'>\n              <bucket>&quot;Reported&quot;</bucket>`,
  `<encoding attr='color' field='[none:nwound_source:nk]' type='palette'>\n            <map to='#bab0ac'>\n              <bucket>&quot;Not Reported&quot;</bucket>\n            </map>\n            <map to='#4e79a7'>\n              <bucket>&quot;Reported&quot;</bucket>`,
  'wound source palette',
);

// Clear, compact worksheet titles.
const worksheetTitles = new Map([
  ['Evoluzione Temporale', 'Eventi e vittime nel tempo'],
  ['Mappa della concentrazione', 'Concentrazione geografica'],
  ['Classifica dei Paesi', 'Paesi con più attentati'],
  ['Mix tattico nel tempo', 'Mix delle tattiche'],
  ['Ascesa dell&apos;attacco suicida', 'Quota di attacchi suicidi'],
  ['Il paradosso frequenza/gravità', 'Frequenza e letalità per tipo di attacco'],
  ['Composizione bersagli per regione', 'Bersagli per regione'],
  ['Mappa frequenza/gravità', 'Frequenza e gravità dei bersagli'],
  ['Matrice Arma x Bersaglio', 'Arma principale e bersaglio principale'],
  ['L&apos;ombra dell&apos;anonimato', 'Quota di autori ignoti nel tempo'],
  ['I protagonisti', 'Gruppi con più attentati attribuiti'],
  ['Firma tattica dei gruppi', 'Firma tattica dei gruppi'],
  ['Provenienza delle misure - Morti', 'Provenienza dei decessi'],
  ['Provenienza delle misure - Feriti', 'Provenienza dei feriti'],
  ['Completezza nel tempo', 'Copertura dei decessi nel tempo'],
  ['Il test di robustezza', "Scarto della letalità dopo l'imputazione"],
]);
for (const [from, to] of worksheetTitles) {
  replaceRequired(`<run>${from}</run>`, `<run>${to}</run>`, `worksheet title ${from}`);
}

// Remove the linear trend line from the suicide time series, retaining the global average reference.
replaceRegexRequired(
  /\n\s*<trendline enable-confidence-bands='false' enable-instant-analytics='true' enabled='true' exclude-color='false' exclude-intercept='false' fit='linear' \/>/g,
  '',
  'suicide trend line',
);

// Dashboard 3 matrix: absolute lethality for colour, distinct events for labels.
replaceRequired(
  `<column-instance column='[eventid]' derivation='Sum' name='[pcto:sum:eventid:qk]' pivot='key' type='quantitative'>\n              <table-calc ordering-type='Rows' type='PctTotal' />\n            </column-instance>`,
  `<column-instance column='[eventid]' derivation='CountD' name='[ctd:eventid:qk]' pivot='key' type='quantitative' />`,
  'matrix event calculation',
);
replaceRequired(
  `<column-instance column='[Calculation_4321186351734784]' derivation='User' name='[pcto:usr:Calculation_4321186351734784:qk]' pivot='key' type='quantitative'>\n              <table-calc ordering-type='Rows' type='PctTotal' />\n            </column-instance>`,
  `<column-instance column='[Calculation_4321186351734784]' derivation='User' name='[usr:Calculation_4321186351734784:qk]' pivot='key' type='quantitative' />`,
  'matrix lethality calculation',
);
replaceRequired(
  '[pcto:usr:Calculation_4321186351734784:qk]',
  '[usr:Calculation_4321186351734784:qk]',
  'matrix absolute lethality references',
  3,
);
replaceRequired('[pcto:sum:eventid:qk]', '[ctd:eventid:qk]', 'matrix distinct event references', 1);

// Dashboard 4 tactical signature starts at macro weapon level; drill paths still expose finer levels.
const ws43Start = xml.indexOf("    <worksheet name='Foglio 4.3'>");
const ws43End = xml.indexOf("    <worksheet name='Foglio 5.1 - A'>", ws43Start);
if (ws43Start < 0 || ws43End < 0) throw new Error('Worksheet 4.3 block not found');
let ws43 = xml.slice(ws43Start, ws43End);
ws43 = ws43
  .replaceAll('[weapon_name]', '[weapon_macro]')
  .replaceAll('[none:weapon_name:nk]', '[none:weapon_macro:nk]')
  .replaceAll("caption='Arma'", "caption='Macro-arma'");
xml = xml.slice(0, ws43Start) + ws43 + xml.slice(ws43End);

// Dashboard 5 robustness view becomes a direct regional percentage delta.
const ws53Start = xml.indexOf("    <worksheet name='Foglio 5.3'>");
const ws53End = xml.indexOf('  </worksheets>', ws53Start);
if (ws53Start < 0 || ws53End < 0) throw new Error('Worksheet 5.3 block not found');
const ws53 = `    <worksheet name='Foglio 5.3'>
      <layout-options>
        <title>
          <formatted-text>
            <run>Scarto della letalità dopo l'imputazione</run>
          </formatted-text>
        </title>
      </layout-options>
      <table>
        <view>
          <datasources>
            <datasource caption='GTD Star' name='federated.1uwnzur0evf63z12rs1zj14huhen' />
          </datasources>
          <datasource-dependencies datasource='federated.1uwnzur0evf63z12rs1zj14huhen'>
            <column caption='Letalità media' datatype='real' default-format='n#,##0.00;-#,##0.00' name='[Calculation_4321186351734784]' role='measure' type='quantitative'>
              <calculation class='tableau' formula='SUM([nkill]) / COUNTD([eventid])' />
            </column>
            <column caption='Letalità solo osservata' datatype='real' default-format='n#,##0.00;-#,##0.00' name='[Calculation_4321186352193541]' role='measure' type='quantitative'>
              <calculation class='tableau' formula='SUM(IIF([nkill_source] = &apos;Reported&apos;, [nkill], 0))&#10;/&#10;COUNTD(IIF([nkill_source] = &apos;Reported&apos;, [eventid], NULL))' />
            </column>
            <column caption='Scarto' datatype='real' default-format='p0.0%' name='[Calculation_4321186730876940]' role='measure' type='quantitative'>
              <calculation class='tableau' formula='([Calculation_4321186351734784]-[Calculation_4321186352193541]) / [Calculation_4321186352193541]' />
            </column>
            <column caption='Precisione della data' datatype='string' name='[date_accuracy]' role='dimension' type='nominal' />
            <column caption='Fonte dei decessi' datatype='string' name='[nkill_source]' role='dimension' type='nominal' />
            <column-instance column='[date_accuracy]' derivation='None' name='[none:date_accuracy:nk]' pivot='key' type='nominal' />
            <column-instance column='[region_name]' derivation='None' name='[none:region_name:nk]' pivot='key' type='nominal' />
            <column caption='Regione' datatype='string' name='[region_name]' role='dimension' semantic-role='[State].[Name]' type='nominal' />
            <column-instance column='[Calculation_4321186351734784]' derivation='User' name='[usr:Calculation_4321186351734784:qk]' pivot='key' type='quantitative' />
            <column-instance column='[Calculation_4321186352193541]' derivation='User' name='[usr:Calculation_4321186352193541:qk]' pivot='key' type='quantitative' />
            <column-instance column='[Calculation_4321186730876940]' derivation='User' name='[usr:Calculation_4321186730876940:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <filter class='categorical' column='[federated.1uwnzur0evf63z12rs1zj14huhen].[none:region_name:nk]' context='true' filter-group='10'>
            <groupfilter function='level-members' level='[none:region_name:nk]' user:ui-enumeration='all' user:ui-marker='enumerate' />
          </filter>
          <computed-sort column='[federated.1uwnzur0evf63z12rs1zj14huhen].[none:region_name:nk]' direction='DESC' using='[federated.1uwnzur0evf63z12rs1zj14huhen].[usr:Calculation_4321186730876940:qk]' />
          <slices>
            <column>[federated.1uwnzur0evf63z12rs1zj14huhen].[none:region_name:nk]</column>
            <column>[federated.1uwnzur0evf63z12rs1zj14huhen].[none:date_accuracy:nk]</column>
          </slices>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view><breakdown value='auto' /></view>
            <mark class='Bar' />
            <encodings>
              <text column='[federated.1uwnzur0evf63z12rs1zj14huhen].[usr:Calculation_4321186730876940:qk]' />
              <tooltip column='[federated.1uwnzur0evf63z12rs1zj14huhen].[usr:Calculation_4321186351734784:qk]' />
              <tooltip column='[federated.1uwnzur0evf63z12rs1zj14huhen].[usr:Calculation_4321186352193541:qk]' />
            </encodings>
            <style>
              <style-rule element='mark'>
                <format attr='mark-color' value='#d99000' />
                <format attr='mark-labels-show' value='true' />
                <format attr='mark-labels-cull' value='true' />
              </style-rule>
            </style>
          </pane>
        </panes>
        <rows>[federated.1uwnzur0evf63z12rs1zj14huhen].[none:region_name:nk]</rows>
        <cols>[federated.1uwnzur0evf63z12rs1zj14huhen].[usr:Calculation_4321186730876940:qk]</cols>
      </table>
      <simple-id uuid='{82C6A36E-BE3A-4687-94A1-6A9B52ABEE3A}' />
    </worksheet>
`;
xml = xml.slice(0, ws53Start) + ws53 + xml.slice(ws53End);

// Exclude null years from the completeness series to remove Tableau's null indicator.
const ws52Start = xml.indexOf("    <worksheet name='Foglio 5.2'>");
const ws52End = xml.indexOf("    <worksheet name='Foglio 5.3'>", ws52Start);
if (ws52Start < 0 || ws52End < 0) throw new Error('Worksheet 5.2 block not found');
let ws52 = xml.slice(ws52Start, ws52End);
const slicesToken = '          <slices>';
if (!ws52.includes(slicesToken)) throw new Error('Worksheet 5.2 slices not found');
ws52 = ws52.replace(
  slicesToken,
  "          <filter class='quantitative' column='[federated.1uwnzur0evf63z12rs1zj14huhen].[tyr:full_date:qk]' included-values='non-null' />\n" +
    slicesToken,
);
xml = xml.slice(0, ws52Start) + ws52 + xml.slice(ws52End);

// Narrative dashboard titles with one compact, evidence-backed annotation each.
const dashboardTitles = new Map([
  [
    'Il perimetro globale: dove e quando',
    'I conteggi crescono, ma il 1993 ricorda che la copertura cambia&#10;209.706 eventi, 523.944 vittime; il vuoto del 1993 è documentale',
  ],
  [
    'L&apos;evoluzione tattica: frequenza contro gravità',
    'Gli attacchi suicidi sono rari ma 4,6 volte più letali&#10;10,17 vittime per attentato contro 2,21 negli altri eventi',
  ],
  [
    'Chi viene colpito: la matrice dei bersagli',
    'La frequenza dei bersagli non coincide con la loro gravità&#10;Civili: 2,95 vittime per evento; bersagli economici: 1,17',
  ],
  [
    'Gli attori: l&apos;ombra dell&apos;anonimato',
    'Il 43,8% degli attentati non ha un autore identificato&#10;Le classifiche per gruppo descrivono una selezione non casuale degli eventi',
  ],
  [
    'La qualità del dato: test di robustezza',
    'Il 5,97% degli eventi usa una stima dei decessi&#10;Lo scarto sulla letalità varia per regione e resta visibile nel warehouse',
  ],
]);
for (const [oldTitle, combined] of dashboardTitles) {
  const [headline, subline] = combined.split('&#10;');
  const replacement = `<run bold='true' fontcolor='#111827' fontname='Tableau Bold' fontsize='20'>${headline}</run><run>&#10;</run><run fontcolor='#5b6573' fontname='Tableau Book' fontsize='10'>${subline}</run>`;
  const re = new RegExp(
    `<run bold='true' fontcolor='#000000' fontname='Tableau Bold' fontsize='24'>${oldTitle.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}<\\/run>(?:\\s*<run>Æ?&#10;<\\/run>)?`,
    'g',
  );
  replaceRegexRequired(re, replacement, `dashboard title ${oldTitle}`, 2);
}

// Keep two visible filters per dashboard and remove redundant legends.
const prefix = '[federated.1uwnzur0evf63z12rs1zj14huhen]';
rewriteDashboard('Dashboard 1', 'Dashboard 2', (block) =>
  removeZonesByParam(block, [
    `${prefix}.[none:nkill_source:nk]`,
    `${prefix}.[:Measure Names]`,
    `${prefix}.[ctd:eventid:qk]`,
  ]),
);
rewriteDashboard('Dashboard 2', 'Dashboard 3', (block) =>
  removeZonesByParam(block, [`${prefix}.[none:target_macro:nk]`]),
);
rewriteDashboard('Dashboard 3', 'Dashboard 4', (block) =>
  removeZonesByParam(block, [
    `${prefix}.[none:weapon_macro:nk]`,
    `${prefix}.[none:is_suicide:ok]`,
    `${prefix}.[sum:nkill:qk]`,
  ]),
);
rewriteDashboard('Dashboard 4', 'Dashboard 5', (block) =>
  removeZonesByParam(block, [
    `${prefix}.[none:attack_macro:nk]`,
    `${prefix}.[usr:Calculation_4321186351734784:qk]`,
  ]),
);
rewriteDashboard('Dashboard 5', null, (block) =>
  removeZonesByParam(block, [`${prefix}.[:Measure Names]`]),
);

// Remove stale Dashboard 5 legend references to Measure Names after the robustness redesign.
xml = xml.replace(
  /\n\s*<zone(?=[^>]*name='Foglio 5\.3')(?=[^>]*type-v2='color')[^>]*>[\s\S]*?<\/zone>/g,
  '',
);

await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.writeFile(outputPath, xml, 'utf8');
console.log(outputPath);
