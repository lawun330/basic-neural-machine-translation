const inputEl = document.getElementById("input");
const outputEl = document.getElementById("output");
const normalizedEl = document.getElementById("normalized");
const modelEl = document.getElementById("model");
const translateBtn = document.getElementById("translate");
const clearBtn = document.getElementById("clear");
const statusEl = document.getElementById("status");
const examplesEl = document.getElementById("examples");

const EXAMPLES = [
  "တက် တက် ပြောင်",
  "ပြာ သာဒ် ဆောင်",
  "ကိုယ် ပိုင် စာ ကြည့် တိုက်",
  "ရွှေ ပြည် စိုး",
  "အ စစ်",
];

function setStatus(message, kind = "") {
  statusEl.textContent = message;
  statusEl.className = `status ${kind}`.trim();
}

async function loadModels() {
  const res = await fetch("/api/models");
  const data = await res.json();
  modelEl.innerHTML = "";

  for (const model of data.models) {
    const opt = document.createElement("option");
    opt.value = model.id;
    opt.textContent = model.label;
    modelEl.appendChild(opt);
  }

  if (data.default) {
    modelEl.value = data.default.id;
  }
}

async function runTranslate() {
  const text = inputEl.value.trim();
  if (!text) {
    setStatus("Enter Burmese syllables first.", "error");
    inputEl.focus();
    return;
  }

  translateBtn.disabled = true;
  setStatus("Translating…");

  try {
    const res = await fetch("/api/translate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text,
        model: modelEl.value,
      }),
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || "Translation failed.");
    }

    outputEl.value = data.phonemes;
    normalizedEl.textContent = data.normalized;
    setStatus("Done.", "ok");
  } catch (err) {
    outputEl.value = "";
    normalizedEl.textContent = "—";
    setStatus(err.message, "error");
  } finally {
    translateBtn.disabled = false;
  }
}

function clearAll() {
  inputEl.value = "";
  outputEl.value = "";
  normalizedEl.textContent = "—";
  setStatus("");
  inputEl.focus();
}

function renderExamples() {
  for (const text of EXAMPLES) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = text;
    btn.addEventListener("click", () => {
      inputEl.value = text;
      runTranslate();
    });
    examplesEl.appendChild(btn);
  }
}

translateBtn.addEventListener("click", runTranslate);
clearBtn.addEventListener("click", clearAll);

inputEl.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
    event.preventDefault();
    runTranslate();
  }
});

loadModels().catch((err) => setStatus(err.message, "error"));
renderExamples();
