import express from "express";
import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

const app = express();
const PORT = Number(process.env.PORT || 3000);

app.use(express.json());
app.use(express.static("public"));

function safeStr(v, fallback = "N/A") {
    if (v === null || v === undefined) return fallback;
    const s = String(v).trim();
    return s.length ? s : fallback;
}

function safeNum(v, fallback = null) {
    const n = Number(v);
    return Number.isFinite(n) ? n : fallback;
}

async function fetchRandomUser() {
    const url = "https://randomuser.me/api/";
    const { data } = await axios.get(url, { timeout: 10000 });
    const u = data?.results?.[0];
    if (!u) throw new Error("RandomUser returned empty result");

    const streetName = u?.location?.street?.name;
    const streetNumber = u?.location?.street?.number;

    return {
        firstName: safeStr(u?.name?.first),
        lastName: safeStr(u?.name?.last),
        gender: safeStr(u?.gender),
        picture: safeStr(u?.picture?.large, ""),
        age: safeNum(u?.dob?.age),
        dob: safeStr(u?.dob?.date),
        city: safeStr(u?.location?.city),
        country: safeStr(u?.location?.country),
        fullAddress: `${safeStr(streetName)} ${safeStr(streetNumber)}`
    };
}

async function fetchCountryInfo(countryName) {
    const restKey = process.env.RESTCOUNTRIES_API_KEY; // "используем" (требование)
    const url = `https://restcountries.com/v3.1/name/${encodeURIComponent(countryName)}?fullText=true`;

    const { data } = await axios.get(url, {
        timeout: 10000,
        headers: restKey ? { "x-api-key": restKey } : {}
    });

    const c = Array.isArray(data) ? data[0] : null;
    if (!c) throw new Error("REST Countries returned empty result");

    const name = c?.name?.common ?? c?.name?.official;
    const capital = Array.isArray(c?.capital) ? c.capital[0] : c?.capital;

    const languagesObj = c?.languages || {};
    const languages = Object.values(languagesObj).map((x) => safeStr(x)).filter(Boolean);

    const currenciesObj = c?.currencies || {};
    const currencyCodes = Object.keys(currenciesObj);
    const currencyCode = currencyCodes[0] || null;
    const currencyName = currencyCode ? safeStr(currenciesObj[currencyCode]?.name) : "N/A";

    const flagPng = c?.flags?.png || c?.flags?.svg || "";

    return {
        countryName: safeStr(name),
        capital: safeStr(capital),
        languages: languages.length ? languages : ["N/A"],
        currency: {
            code: currencyCode || "N/A",
            name: currencyName
        },
        flag: safeStr(flagPng, "")
    };
}

async function fetchExchangeRates(baseCurrency) {
    const key = process.env.EXCHANGE_RATE_API_KEY;
    if (!key) {
        return {
            base: baseCurrency,
            USD: null,
            KZT: null,
            message: "No EXCHANGE_RATE_API_KEY in .env"
        };
    }

    const url = `https://v6.exchangerate-api.com/v6/${key}/latest/${encodeURIComponent(baseCurrency)}`;
    const { data } = await axios.get(url, { timeout: 10000 });

    const rates = data?.conversion_rates || {};
    const usd = safeNum(rates?.USD);
    const kzt = safeNum(rates?.KZT);

    return {
        base: baseCurrency,
        USD: usd,
        KZT: kzt,
        message: null
    };
}

async function fetchNews(countryName) {
    const key = process.env.NEWS_API_KEY;
    if (!key) {
        return { items: [], message: "No NEWS_API_KEY in .env" };
    }

    const url =
        `https://newsapi.org/v2/everything?` +
        `q=${encodeURIComponent(countryName)}&language=en&pageSize=20&sortBy=publishedAt&apiKey=${key}`;

    const { data } = await axios.get(url, { timeout: 10000 });

    const articles = Array.isArray(data?.articles) ? data.articles : [];
    const re = new RegExp(countryName.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "i");

    const filtered = articles
        .filter((a) => re.test(a?.title || ""))
        .slice(0, 5)
        .map((a) => ({
            title: safeStr(a?.title),
            description: safeStr(a?.description),
            image: safeStr(a?.urlToImage, ""),
            url: safeStr(a?.url, ""),
            source: safeStr(a?.source?.name)
        }));

    return { items: filtered, message: null };
}

app.get("/api/profile", async (req, res) => {
    try {
        const user = await fetchRandomUser();

        let country = null;
        try {
            country = await fetchCountryInfo(user.country);
        } catch (e) {
            country = {
                countryName: user.country,
                capital: "N/A",
                languages: ["N/A"],
                currency: { code: "N/A", name: "N/A" },
                flag: ""
            };
        }

        let rates = null;
        if (country?.currency?.code && country.currency.code !== "N/A") {
            rates = await fetchExchangeRates(country.currency.code);
        } else {
            rates = { base: "N/A", USD: null, KZT: null, message: "No currency code found" };
        }

        const news = await fetchNews(user.country);

        res.json({
            ok: true,
            user,
            country,
            exchange: rates,
            news
        });
    } catch (err) {
        res.status(500).json({
            ok: false,
            error: err?.message || "Server error"
        });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
