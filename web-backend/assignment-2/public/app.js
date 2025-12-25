const btn = document.getElementById("btn");
const statusEl = document.getElementById("status");

const userCard = document.getElementById("userCard");
const countryCard = document.getElementById("countryCard");
const newsBlock = document.getElementById("newsBlock");

function setStatus(text) {
    statusEl.textContent = text || "";
}

function escapeHtml(s) {
    return String(s)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function renderUser(u) {
    const img = u.picture ? `<img class="avatar" src="${escapeHtml(u.picture)}" alt="Profile" />` : "";
    userCard.innerHTML = `
    <h2>User</h2>
    <div class="row">
      ${img}
      <div>
        <div><b>First name:</b> ${escapeHtml(u.firstName)}</div>
        <div><b>Last name:</b> ${escapeHtml(u.lastName)}</div>
        <div><b>Gender:</b> ${escapeHtml(u.gender)}</div>
        <div><b>Age:</b> ${u.age ?? "N/A"}</div>
        <div><b>Date of birth:</b> ${escapeHtml(u.dob)}</div>
        <div><b>City:</b> ${escapeHtml(u.city)}</div>
        <div><b>Country:</b> ${escapeHtml(u.country)}</div>
        <div><b>Full address:</b> ${escapeHtml(u.fullAddress)}</div>
      </div>
    </div>
  `;
}

function renderCountry(c, exchange) {
    const flag = c.flag ? `<img class="flag" src="${escapeHtml(c.flag)}" alt="Flag" />` : "";
    const langs = Array.isArray(c.languages) ? c.languages.join(", ") : "N/A";

    let rateLine = "";
    if (exchange?.base && exchange.base !== "N/A" && exchange.USD && exchange.KZT) {
        rateLine = `
      <div class="box">
        <h3>Exchange rates</h3>
        <div><b>1 ${escapeHtml(exchange.base)}</b> = ${exchange.USD} USD</div>
        <div><b>1 ${escapeHtml(exchange.base)}</b> = ${exchange.KZT} KZT</div>
      </div>
    `;
    } else {
        const msg = exchange?.message ? ` (${escapeHtml(exchange.message)})` : "";
        rateLine = `
      <div class="box">
        <h3>Exchange rates</h3>
        <div>Rates not available${msg}</div>
      </div>
    `;
    }

    countryCard.innerHTML = `
    <h2>Country</h2>
    <div class="row">
      ${flag}
      <div>
        <div><b>Country name:</b> ${escapeHtml(c.countryName)}</div>
        <div><b>Capital:</b> ${escapeHtml(c.capital)}</div>
        <div><b>Languages:</b> ${escapeHtml(langs)}</div>
        <div><b>Currency:</b> ${escapeHtml(c.currency?.code)} (${escapeHtml(c.currency?.name)})</div>
      </div>
    </div>
    ${rateLine}
  `;
}

function renderNews(news) {
    const items = news?.items || [];
    const msg = news?.message ? `<p class="muted">${escapeHtml(news.message)}</p>` : "";

    if (!items.length) {
        newsBlock.innerHTML = `
      <h2>News</h2>
      ${msg}
      <p class="muted">No matching headlines found.</p>
    `;
        return;
    }

    const cards = items
        .map((n) => {
            const img = n.image ? `<img class="newsImg" src="${escapeHtml(n.image)}" alt="news" />` : "";
            const link = n.url ? `<a href="${escapeHtml(n.url)}" target="_blank" rel="noreferrer">Open article</a>` : "";
            return `
        <article class="newsCard">
          ${img}
          <div>
            <h4>${escapeHtml(n.title)}</h4>
            <p class="muted">${escapeHtml(n.description)}</p>
            <div class="muted">Source: ${escapeHtml(n.source)}</div>
            ${link}
          </div>
        </article>
      `;
        })
        .join("");

    newsBlock.innerHTML = `
    <h2>News (5 headlines)</h2>
    ${msg}
    <div class="newsList">${cards}</div>
  `;
}

async function loadProfile() {
    setStatus("Loading...");
    btn.disabled = true;

    userCard.innerHTML = "";
    countryCard.innerHTML = "";
    newsBlock.innerHTML = "";

    try {
        const res = await fetch("/api/profile");
        const data = await res.json();

        if (!data.ok) throw new Error(data.error || "Request failed");

        renderUser(data.user);
        renderCountry(data.country, data.exchange);
        renderNews(data.news);

        setStatus("Done.");
    } catch (e) {
        setStatus("Error: " + (e?.message || "Unknown error"));
    } finally {
        btn.disabled = false;
    }
}

btn.addEventListener("click", loadProfile);
