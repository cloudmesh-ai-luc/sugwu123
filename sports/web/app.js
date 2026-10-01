"use strict";
const byId = id => document.getElementById(id);
const form = byId("filters");
const percent = value => value === null ? "No data" : `${(100 * value).toFixed(1)}%`;
const decimal = value => value === null ? "Insufficient history" : value.toFixed(3);
let choices;
let requestNumber = 0;

async function api(path) {
  const response = await fetch(path);
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || "Unable to load analysis");
  return result;
}

function options(element, values, allLabel) {
  element.replaceChildren();
  if (allLabel) element.add(new Option(allLabel, ""));
  for (const value of values) element.add(new Option(value, value));
}

function teamChanged() {
  const team = byId("team").value;
  options(byId("player"), choices.players_by_team[team] || [], "Team total");
  options(byId("opponent"), choices.opponents_by_team[team] || [], "All opponents");
  byId("threshold").value = "100.5";
}

function svgElement(name, attributes, text) {
  const element = document.createElementNS("http://www.w3.org/2000/svg", name);
  for (const [key, value] of Object.entries(attributes)) element.setAttribute(key, value);
  if (text !== undefined) element.textContent = text;
  return element;
}

function plot(series, threshold) {
  const chart = byId("chart");
  chart.replaceChildren();
  if (!series.length) {
    chart.append(svgElement("text", {x: 50, y: 100, class: "chart-label"}, "No observations for these filters"));
    return;
  }
  const maximum = Math.max(threshold, ...series.map(row => row.value), 1) * 1.12;
  const x = index => 55 + (series.length === 1 ? 425 : index * 850 / (series.length - 1));
  const y = value => 218 - 190 * value / maximum;
  for (let index = 0; index <= 4; index++) {
    const value = maximum * index / 4;
    chart.append(svgElement("line", {x1: 55, x2: 905, y1: y(value), y2: y(value), stroke: "#e0e7ed"}));
    chart.append(svgElement("text", {x: 45, y: y(value) + 4, "text-anchor": "end", class: "chart-label"}, value.toFixed(0)));
  }
  chart.append(svgElement("line", {x1: 55, x2: 905, y1: y(threshold), y2: y(threshold), stroke: "#b18427", "stroke-dasharray": "6 5"}));
  chart.append(svgElement("polyline", {points: series.map((row, index) => `${x(index)},${y(row.value)}`).join(" "), fill: "none", stroke: "#24618a", "stroke-width": 3}));
  series.forEach((row, index) => {
    const dot = svgElement("circle", {cx: x(index), cy: y(row.value), r: 4, fill: "#24618a"});
    dot.append(svgElement("title", {}, `${row.date}: ${row.value} points vs ${row.opponent}`));
    chart.append(dot);
  });
  chart.append(svgElement("text", {x: 55, y: 245, class: "chart-label"}, series[0].date));
  if (series.length > 1) chart.append(svgElement("text", {x: 905, y: 245, "text-anchor": "end", class: "chart-label"}, series[series.length - 1].date));
  chart.append(svgElement("text", {x: 480, y: 266, "text-anchor": "middle", class: "chart-label"}, "Game sequence"));
}

function render(result) {
  const summary = result.summary;
  const selection = result.selection;
  byId("selection").textContent = selection.player || selection.team;
  byId("metric").textContent = selection.metric;
  byId("rate").textContent = percent(summary.historical_rate);
  byId("events").textContent = `${summary.exceeded_threshold} of ${summary.games} games above ${selection.threshold} points`;
  byId("interval").textContent = summary.wilson_95_interval ? summary.wilson_95_interval.map(percent).join(" to ") : "No data";
  byId("average").textContent = summary.mean_points === null ? "No data" : summary.mean_points.toFixed(1);
  byId("sample").textContent = `${summary.games} selected games`;
  byId("record").textContent = `${summary.wins} / ${summary.losses} / ${summary.draws}`;
  byId("evaluated").textContent = result.evaluation.evaluated_games;
  byId("brier").textContent = decimal(result.evaluation.brier_score);
  byId("baseline").textContent = decimal(result.evaluation.constant_half_brier_score);
  byId("interpretation").textContent = result.interpretation;
  byId("chart-title").textContent = `${selection.metric} by game`;
  plot(result.series, selection.threshold);
  const body = byId("observations");
  body.replaceChildren();
  for (const row of result.series.slice(-10).reverse()) {
    const tr = document.createElement("tr");
    for (const value of [row.date, row.opponent, row.value]) {
      const td = document.createElement("td");
      td.textContent = value;
      tr.append(td);
    }
    body.append(tr);
  }
  byId("results").hidden = false;
}

async function refresh() {
  const request = ++requestNumber;
  const button = form.querySelector("button");
  button.disabled = true;
  byId("message").textContent = "";
  byId("results").hidden = true;
  try {
    const parameters = new URLSearchParams({team: byId("team").value, player: byId("player").value,
      opponent: byId("opponent").value, threshold: byId("threshold").value});
    const result = await api(`/api/analyze?${parameters}`);
    if (request === requestNumber) render(result);
  } catch (error) {
    if (request === requestNumber) byId("message").textContent = error.message;
  } finally {
    if (request === requestNumber) button.disabled = false;
  }
}

form.addEventListener("submit", event => {event.preventDefault(); refresh();});
byId("team").addEventListener("change", () => {teamChanged(); refresh();});
byId("player").addEventListener("change", () => {byId("threshold").value = byId("player").value ? "20.5" : "100.5"; refresh();});
byId("opponent").addEventListener("change", refresh);

(async () => {
  try {
    choices = await api("/api/options");
    const dataset = choices.dataset;
    byId("dataset").textContent = dataset.kind === "synthetic"
      ? "Fictional basketball demo data. These numbers are generated examples, not real team or player statistics."
      : dataset.kind === "empty" ? "No dataset loaded. Use the documented CLI to generate a demo or import historical data."
      : `Imported data | Source: ${dataset.source} | Rights: ${dataset.rights}`;
    options(byId("team"), choices.teams);
    if (choices.teams.length) {teamChanged(); await refresh();}
    else form.querySelector("button").disabled = true;
  } catch (error) {
    byId("message").textContent = error.message;
  }
})();
