// ===============================
//   MULTI-STEP FORM (SCREENING)
// ===============================
(function () {
  let currentStepIndex = 0;
  let formSteps = [];
  let totalSteps = 0;

  function init() {
    formSteps = Array.from(document.querySelectorAll(".form-step"));
    totalSteps = formSteps.length;

    const totalStepsEl = document.getElementById("totalSteps");
    if (totalStepsEl) totalStepsEl.textContent = totalSteps;

    console.log("screening app init, total steps =", totalSteps);
    showStep(0);
  }

  function showStep(index) {
    if (!formSteps.length) return;
    currentStepIndex = Math.max(0, Math.min(index, totalSteps - 1));

    formSteps.forEach((el, i) => {
      el.style.display = i === currentStepIndex ? "" : "none";
    });

    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");

    if (prevBtn) prevBtn.style.display = currentStepIndex === 0 ? "none" : "";

    if (nextBtn) {
      if (currentStepIndex === totalSteps - 1) {
        nextBtn.textContent = "Proses Prediksi";
        nextBtn.type = "button";
      } else {
        nextBtn.textContent = "Selanjutnya";
        nextBtn.type = "button";
      }
    }

    const currentStepEl = document.getElementById("currentStep");
    if (currentStepEl) currentStepEl.textContent = currentStepIndex + 1;

    const progressFill = document.getElementById("progressFill");
    if (progressFill) {
      const pct = Math.round(((currentStepIndex + 1) / totalSteps) * 100);
      progressFill.style.width = pct + "%";
    }

    try {
      if (currentStepIndex === totalSteps - 1) {
        buildSummary();
      }
    } catch (e) {
      console.warn("buildSummary error", e);
    }
  }

  function validateStep(index) {
    const step = formSteps[index];
    if (!step) return true;

    const requiredEls = Array.from(step.querySelectorAll("[required]"));
    for (const el of requiredEls) {
      const val = el.value;
      if (el.tagName === "SELECT") {
        if (!val) {
          el.focus();
          return false;
        }
      } else if (el.type === "checkbox" || el.type === "radio") {
        const name = el.name;
        if (name) {
          const group = step.querySelectorAll('[name="' + name + '"]');
          const any = Array.from(group).some((g) => g.checked);
          if (!any) {
            el.focus();
            return false;
          }
        }
      } else {
        if (val === null || val === undefined || String(val).trim() === "") {
          el.focus();
          return false;
        }
      }
    }
    return true;
  }

  window.nextStep = function () {
    if (!formSteps.length) return;

    if (currentStepIndex === totalSteps - 1) {
      const form = document.getElementById("screeningForm");
      if (form) form.submit();
      return;
    }

    if (!validateStep(currentStepIndex)) {
      alert("Mohon lengkapi semua field wajib pada halaman ini sebelum melanjutkan.");
      return;
    }

    showStep(currentStepIndex + 1);
  };

  window.previousStep = function () {
    if (!formSteps.length) return;
    showStep(currentStepIndex - 1);
  };

  function fmtBool(val) {
    if (val === null || val === undefined || val === "") return "-";
    const s = String(val);
    if (["1", "true", "ya"].includes(s.toLowerCase())) return "Ya";
    if (["0", "false", "tidak"].includes(s.toLowerCase())) return "Tidak";
    return s;
  }

  function buildSummary() {
    const form = document.getElementById("screeningForm");
    const container = document.getElementById("summaryContent");
    if (!form || !container) return;

    const categories = {
      "Informasi Dasar Pasien": [
        { key: "patient_name", label: "Nama Pasien" },
        { key: "district_city", label: "Kabupaten/Kota" },
        { key: "patient_age", label: "Umur (Tahun)", unit: "tahun" },
        { key: "education_level", label: "Pendidikan" },
        { key: "current_occupation", label: "Perkerjaan " },
        { key: "marital_status", label: "Status Nikah" },
        { key: "marriage_order", label: "Pernikahan Ke" },
        { key: "parity", label: "Paritas" },
      ],
      "Riwayat Kehamilan & Perencanaan": [
        { key: "new_partner_pregnancy", label: "Hamil Pasangan Baru", map: { 0: "Tidak", 1: "Ya" }},
        { key: "child_spacing_over_10_years", label: "Jarak Anak >10 tahun", map: { 0: "Tidak", 1: "Ya" }},
        { key: "ivf_pregnancy", label: "Bayi Tabung", map: { 0: "Tidak", 1: "Ya" }},
        { key: "multiple_pregnancy", label: "Gemelli", map: { 0: "Tidak", 1: "Ya" }},
        { key: "smoker", label: "Perokok", map: { 0: "Tidak", 1: "Ya" }},
        { key: "planned_pregnancy", label: "Hamil Direncanakan", map: { 0: "Tidak", 1: "Ya" }},
      ],
      "Riwayat Pribadi & Penyakit Ibu": [
        { key: "family_history_pe", label: "Riwayat Keluarga Preeklampsia", map: { 0: "Tidak", 1: "Ya" }},
        { key: "personal_history_pe", label: "Riwayat Preeklampsia", map: { 0: "Tidak", 1: "Ya" }},
        { key: "chronic_hypertension", label: "Hipertensi Kronis", map: { 0: "Tidak", 1: "Ya" }},
        { key: "diabetes_mellitus", label: "Diabetes Melitus", map: { 0: "Tidak", 1: "Ya" }},
        { key: "kidney_disease", label: "Riwayat Penyakit Ginjal", map: { 0: "Tidak", 1: "Ya" }},
        { key: "autoimmune_disease", label: "Penyakit Autoimune", map: { 0: "Tidak", 1: "Ya" }},
        { key: "aps_history", label: "APS", map: { 0: "Tidak", 1: "Ya" }},
      ],
      "Antropometri & Pemeriksaan": [
        { key: "pre_pregnancy_weight", label: "BB Sebelum Hamil", unit: "kg" },
        { key: "height_cm", label: "Tinggi Badan", unit: "cm" },
        { key: "bmi", label: "BMI", unit: "kg/m²" },
        { key: "lila_cm", label: "LiLA", unit: "cm" },
        { key: "systolic_bp", label: "TD Sistolik I", unit: "mmHg" },
        { key: "diastolic_bp", label: "TD Diastolik I", unit: "mmHg" },
        { key: "map_mmhg", label: "MAP", unit: "mmHg" },
        { key: "hemoglobin", label: "Hb", unit: "g/dL" },
      ],
      "Riwayat Penyakit Keluarga": [
        { key: "family_history_hypertension", label: "Hipertensi Keluarga", map: { 0: "Tidak", 1: "Ya" }},
        { key: "family_history_kidney", label: "Penyakit Ginjal Keluarga", map: { 0: "Tidak", 1: "Ya" }},
        { key: "family_history_heart", label: "Penyakit Jantung Keluarga", map: { 0: "Tidak", 1: "Ya" }},
      ],
    };

    function getFieldValue(f) {
      const el = form.querySelector('[name="' + f.key + '"]');
      if (!el) return "-";

      let raw = el.value;

      if (el.tagName === "SELECT") {
        if (f.map && f.map[raw] !== undefined) return f.map[raw];
        return el.options[el.selectedIndex]?.text || raw || "-";
      }

      if (el.type === "checkbox" || el.type === "radio") {
        raw = el.checked ? el.value || "1" : "0";
      }

      if (!raw) return "-";
      if (f.map && f.map[raw] !== undefined) return f.map[raw];
      if (f.unit) return raw + " " + f.unit;

      return raw;
    }

    let html = "";

    for (const [cat, fields] of Object.entries(categories)) {
      html += `<div class="summary-section"><h4>${cat}</h4>`;
      fields.forEach((f) => {
        html += `
          <div class="summary-item">
            <span class="summary-label">${f.label}</span>
            <span class="summary-value">${getFieldValue(f)}</span>
          </div>`;
      });
      html += `</div>`;
    }

    container.innerHTML = html;
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

// =======================================
//   DASHBOARD FILTER DI dashboard.html
// =======================================
window.loadDashboardData = function () {
  const search = document.getElementById("search-patient");
  const filterBtn = document.querySelector(".btn-filter");
  const clearBtn = document.querySelector(".btn-clear");

  if (search) {
    search.addEventListener("keyup", (e) => {
      if (e.key === "Enter") filterData();
    });
  }
  if (filterBtn) filterBtn.addEventListener("click", filterData);
  if (clearBtn) clearBtn.addEventListener("click", clearFilters);
};

// FILTER UTAMA
window.filterData = function () {
  console.debug("filterData called");

  const searchTerm = (document.getElementById("search-patient")?.value || "")
    .trim()
    .toLowerCase();

  const resultFilter = (document.getElementById("filter-result")?.value || "")
    .trim()
    .toLowerCase(); // "" / "preeklampsia" / "non-preeklampsia"

  const tbody = document.getElementById("admin-table-body");
  if (!tbody) return;

  const rows = Array.from(tbody.querySelectorAll("tr"));

  rows.forEach((row) => {
    const cells = row.children;
    if (!cells.length) return;

    // Baris placeholder "Belum ada data prediksi"
    if (cells[0].hasAttribute("colspan")) {
      row.style.display = "";
      return;
    }

    // Struktur tabel:
    // 0: No
    // 1: Email
    // 2: Tanggal
    // 3: Nama Pasien
    // ...
    // n-2: Hasil
    // n-1: Confidence
    const nameCell = cells[3];
    // Gunakan class untuk hasil jika ada; fallback ke kolom sebelum terakhir
    const resultCell =
      row.querySelector(".result-cell") || cells[cells.length - 2];

    const nameText = (nameCell?.textContent || "").toLowerCase();
    const hasilTextRaw = (resultCell?.textContent || "").toLowerCase().trim();

    // Normalisasi hasil: hilangkan spasi dan tanda minus
    const hasilNorm = hasilTextRaw.replace(/[\s-]+/g, "");

    let show = true;

    // === Filter berdasarkan nama pasien ===
    if (searchTerm && !nameText.includes(searchTerm)) {
      show = false;
    }

    // === Filter berdasarkan hasil ===
    if (show && resultFilter) {
      const filterNorm = resultFilter.replace(/[\s-]+/g, ""); // "preeklampsia" atau "nonpreeklampsia"

      // Normalisasi hasil: hapus spasi/dash lalu cek apakah mengandung kata kunci
      const hasPree = hasilNorm.includes("preeklampsia") || hasilNorm.includes("preeclampsia");
      const hasNon = hasilNorm.includes("nonpreeklampsia") || hasilNorm.includes("nonpreeclampsia");

      if (filterNorm.startsWith("non")) {
        // minta Non-Preeklampsia -> harus ada 'non' di hasil
        if (!hasNon) show = false;
      } else if (filterNorm.includes("preeclampsia") || filterNorm.includes("preeklampsia")) {
        // minta Preeklampsia -> harus pree dan bukan non
        if (!hasPree || hasNon) show = false;
      }
    }

    row.style.display = show ? "" : "none";
  });
};

// CLEAR FILTER
window.clearFilters = function () {
  const s = document.getElementById("search-patient");
  const rf = document.getElementById("filter-result");

  if (s) s.value = "";
  if (rf) rf.value = "";

  const tbody = document.getElementById("admin-table-body");
  if (tbody) {
    Array.from(tbody.querySelectorAll("tr")).forEach((row) => {
      row.style.display = "";
    });
  }
};
