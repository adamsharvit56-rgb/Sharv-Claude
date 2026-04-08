document.addEventListener("DOMContentLoaded", () => {
  const sourceSelect = document.getElementById("source");
  const regressionSlider = document.getElementById("regression");
  const regressionValue = document.getElementById("regression-value");
  const positionSelect = document.getElementById("position");
  const refreshBtn = document.getElementById("refresh-btn");
  const skatersSection = document.getElementById("skaters-section");
  const goaliesSection = document.getElementById("goalies-section");
  const skatersBody = document.querySelector("#skaters-table tbody");
  const goaliesBody = document.querySelector("#goalies-table tbody");
  const loading = document.getElementById("loading");

  let currentSkaters = [];
  let currentGoalies = [];
  let skaterSort = { key: "fantasy_points", asc: false };
  let goalieSort = { key: "fantasy_points", asc: false };

  // Regression slider label
  regressionSlider.addEventListener("input", () => {
    regressionValue.textContent = (regressionSlider.value / 100).toFixed(2);
  });

  // Sortable headers
  document.querySelectorAll("#skaters-table th.sortable").forEach((th) => {
    th.addEventListener("click", () => {
      const key = th.dataset.sort;
      if (skaterSort.key === key) {
        skaterSort.asc = !skaterSort.asc;
      } else {
        skaterSort.key = key;
        skaterSort.asc = false;
      }
      updateSortIndicators("skaters-table", skaterSort);
      renderSkaters();
    });
  });

  document.querySelectorAll("#goalies-table th.sortable").forEach((th) => {
    th.addEventListener("click", () => {
      const key = th.dataset.sort;
      if (goalieSort.key === key) {
        goalieSort.asc = !goalieSort.asc;
      } else {
        goalieSort.key = key;
        goalieSort.asc = false;
      }
      updateSortIndicators("goalies-table", goalieSort);
      renderGoalies();
    });
  });

  function updateSortIndicators(tableId, sortState) {
    const table = document.getElementById(tableId);
    table.querySelectorAll("th.sortable").forEach((th) => {
      th.classList.remove("active-sort", "asc");
      if (th.dataset.sort === sortState.key) {
        th.classList.add("active-sort");
        if (sortState.asc) th.classList.add("asc");
      }
    });
  }

  function sortData(data, sortState) {
    const sorted = [...data];
    sorted.sort((a, b) => {
      let va = a[sortState.key];
      let vb = b[sortState.key];
      if (typeof va === "string") {
        va = va.toLowerCase();
        vb = vb.toLowerCase();
        return sortState.asc ? va.localeCompare(vb) : vb.localeCompare(va);
      }
      return sortState.asc ? va - vb : vb - va;
    });
    return sorted;
  }

  function rankBadge(rank) {
    if (rank <= 3) {
      return `<span class="rank-badge rank-${rank}">${rank}</span>`;
    }
    return rank;
  }

  function renderSkaters() {
    const sorted = sortData(currentSkaters, skaterSort);
    skatersBody.innerHTML = sorted
      .map(
        (p, i) => `
      <tr>
        <td class="rank-col">${rankBadge(i + 1)}</td>
        <td class="player-col"><span class="player-name">${escapeHtml(p.name)}</span></td>
        <td>${escapeHtml(p.position || "")}</td>
        <td><span class="player-team-badge">${escapeHtml(p.team)}</span></td>
        <td class="num-col">${p.projected_gp}</td>
        <td class="num-col">${p.projected_goals}</td>
        <td class="num-col">${p.projected_assists}</td>
        <td class="num-col stat-highlight">${p.projected_points}</td>
        <td class="num-col stat-highlight">${p.fantasy_points}</td>
      </tr>`
      )
      .join("");
  }

  function renderGoalies() {
    const sorted = sortData(currentGoalies, goalieSort);
    goaliesBody.innerHTML = sorted
      .map(
        (g, i) => `
      <tr>
        <td class="rank-col">${rankBadge(i + 1)}</td>
        <td class="player-col"><span class="player-name">${escapeHtml(g.name)}</span></td>
        <td><span class="player-team-badge">${escapeHtml(g.team)}</span></td>
        <td class="num-col">${g.projected_gp}</td>
        <td class="num-col">${g.projected_wins}</td>
        <td class="num-col">${g.projected_save_pct.toFixed(3)}</td>
        <td class="num-col">${g.projected_gaa.toFixed(2)}</td>
        <td class="num-col">${g.projected_shutouts}</td>
        <td class="num-col stat-highlight">${g.fantasy_points}</td>
      </tr>`
      )
      .join("");
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  async function fetchProjections() {
    const source = sourceSelect.value;
    const regression = (regressionSlider.value / 100).toFixed(2);
    const position = positionSelect.value;

    loading.classList.remove("hidden");
    skatersSection.style.display = "none";
    goaliesSection.style.display = "none";

    try {
      const resp = await fetch(
        `/api/projections?source=${source}&regression=${regression}&position=${position}`
      );
      const data = await resp.json();

      currentSkaters = data.skaters || [];
      currentGoalies = data.goalies || [];

      if (currentSkaters.length > 0) {
        skatersSection.style.display = "block";
        renderSkaters();
      }

      if (currentGoalies.length > 0) {
        goaliesSection.style.display = "block";
        renderGoalies();
      }
    } catch (err) {
      skatersBody.innerHTML = `<tr><td colspan="9" style="text-align:center;color:var(--red);padding:24px;">Error loading projections: ${escapeHtml(err.message)}</td></tr>`;
      skatersSection.style.display = "block";
    } finally {
      loading.classList.add("hidden");
    }
  }

  refreshBtn.addEventListener("click", fetchProjections);

  // Load on page open
  fetchProjections();
});
