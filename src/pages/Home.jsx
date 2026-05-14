import { useEffect, useMemo, useState } from "react";
import Filters from "../components/Filters";
import JobList from "../components/JobList";
import Loader from "../components/Loader";
import Error from "../components/Error";
import { fetchJobs, filterJobs, DEMO_JOBS, normalizeType } from "../services/api";
import { useAuth } from "../context/AuthContext";

const CATEGORY_TABS = [
  "Engineering",
  "Design",
  "Marketing",
  "Management",
  "Finance",
];

const HIRING_UPDATES = [
  "Remote engineering roles are moving fastest this week.",
  "Profiles with CV uploads get stronger application visibility.",
  "Employers are shortlisting candidates within 48 hours.",
];

function initials(name = "") {
  const value = String(name).trim();
  if (!value) return "HF";
  return value
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0])
    .join("")
    .toUpperCase();
}

function badgeLabel(type = "") {
  const normalizedType = normalizeType(type);

  const labels = {
    "full-time": "Full-time",
    contract: "Contract",
    "part-time": "Part-time",
    freelance: "Freelance",
    remote: "Remote",
  };

  return labels[normalizedType] || type || "Remote";
}

function Home({
  searchTerm = "",
  setSearchTerm,
  savedIds = new Set(),
  onSave,
  onSelectJob,
  onNavigate,
  activeCategory = "All",
  setActiveCategory,
}) {
  const { user, isAuthenticated } = useAuth();
  const [allJobs, setAllJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterType, setFilterType] = useState("");
  const [lastUpdated, setLastUpdated] = useState("");

  const loadJobs = async () => {
    setLoading(true);
    setError(null);

    try {
      const jobs = await fetchJobs({
        search: searchTerm,
        category: activeCategory,
        limit: 60,
      });
      setAllJobs(Array.isArray(jobs) && jobs.length > 0 ? jobs : DEMO_JOBS);
      setLastUpdated(new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }));
    } catch (err) {
      setError(err?.message || "Failed to load jobs.");
      setAllJobs(DEMO_JOBS);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let isMounted = true;

    const run = async () => {
      setLoading(true);
      setError(null);

      try {
        const jobs = await fetchJobs({ limit: 60 });

        if (isMounted) {
          setAllJobs(Array.isArray(jobs) && jobs.length > 0 ? jobs : DEMO_JOBS);
          setLastUpdated(new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }));
        }
      } catch (err) {
        if (!isMounted) return;

        setError(err?.message || "Failed to load jobs.");
        setAllJobs(DEMO_JOBS);
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    run();

    return () => {
      isMounted = false;
    };
  }, []);

  const filteredJobs = useMemo(() => {
    return filterJobs(allJobs, {
      searchTerm,
      category: activeCategory,
      filterType,
    });
  }, [allJobs, searchTerm, activeCategory, filterType]);

  const featuredJobs = useMemo(() => {
    const featured = filteredJobs.filter((job) => job.featured).slice(0, 3);
    return featured.length > 0 ? featured : filteredJobs.slice(0, 3);
  }, [filteredJobs]);

  const companies = useMemo(() => {
    const uniqueCompanies = new Map();

    allJobs.forEach((job) => {
      if (!job?.company || uniqueCompanies.has(job.company)) return;
      uniqueCompanies.set(job.company, job);
    });

    return [...uniqueCompanies.values()].slice(0, 5);
  }, [allJobs]);

  const stats = useMemo(() => {
    const companyCount = new Set(allJobs.map((job) => job?.company).filter(Boolean)).size;
    const remoteCount = allJobs.filter((job) =>
      String(job?.location || "").toLowerCase().includes("remote")
    ).length;

    return {
      total: allJobs.length,
      companies: companyCount,
      remote: remoteCount,
      saved: savedIds.size,
    };
  }, [allJobs, savedIds]);

  const handleSearchChange = (event) => {
    setSearchTerm?.(event.target.value);
  };

  const handleSearchSubmit = (event) => {
    event.preventDefault();
    document.getElementById("jobs-anchor")?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  };

  return (
    <div className="page page--home professional-home">
      <section className="pro-shell">
        <div className="container pro-grid">
          <aside className="pro-sidebar">
            <div className="profile-card">
              <div className="profile-card__cover" />
              <div className="profile-card__avatar">
                {initials(user?.username || "HireFlow")}
              </div>
              <h2>{isAuthenticated ? user?.username : "Build your profile"}</h2>
              <p>
                {isAuthenticated
                  ? `${user?.role?.replace("_", " ")} account`
                  : "Sign in to save jobs, upload your CV, and apply faster."}
              </p>
              <button
                type="button"
                className="btn btn--primary profile-card__cta"
                onClick={() => onNavigate?.(isAuthenticated ? "profile" : "login")}
              >
                {isAuthenticated ? "View profile" : "Sign in"}
              </button>
            </div>

            <div className="side-card">
              <h3>Career snapshot</h3>
              <div className="side-stat">
                <span>Saved jobs</span>
                <strong>{stats.saved}</strong>
              </div>
              <div className="side-stat">
                <span>Open roles</span>
                <strong>{stats.total}</strong>
              </div>
              <div className="side-stat">
                <span>Hiring companies</span>
                <strong>{stats.companies}</strong>
              </div>
            </div>
          </aside>

          <main className="pro-main">
            <div className="feed-composer">
              <div className="feed-composer__top">
                <div className="mini-avatar">{initials(user?.username || "HF")}</div>
                <form className="feed-search" onSubmit={handleSearchSubmit}>
                  <input
                    type="search"
                    placeholder="Search jobs, companies, skills"
                    value={searchTerm}
                    onChange={handleSearchChange}
                  />
                  <button type="submit">Search</button>
                </form>
              </div>

              <div className="feed-composer__actions">
                {CATEGORY_TABS.map((category) => (
                  <button
                    type="button"
                    key={category}
                    onClick={() => {
                      setActiveCategory?.(category.toLowerCase());
                      document.getElementById("jobs-anchor")?.scrollIntoView({ behavior: "smooth" });
                    }}
                  >
                    {category}
                  </button>
                ))}
              </div>
            </div>

            <div className="feed-card feed-card--hero">
              <div>
                <p className="feed-card__eyebrow">Live hiring desk</p>
                <h1>Find roles, follow companies, and apply from one professional workspace.</h1>
                <p>
                  HireFlow now blends your local backend jobs with public listings at
                  the same time, then removes duplicates before showing matches.
                </p>
              </div>
              <div className="feed-card__metrics">
                <span><strong>{stats.total}</strong> roles</span>
                <span><strong>{stats.remote}</strong> remote</span>
                <span><strong>{lastUpdated || "Live"}</strong> sync</span>
              </div>
            </div>

            <div className="feed-card">
              <div className="feed-card__head">
                <div>
                  <p className="feed-card__eyebrow">Recommended for you</p>
                  <h2>Fast-moving jobs</h2>
                </div>
                <button type="button" onClick={() => onNavigate?.("jobs")}>View all</button>
              </div>

              <div className="recommendation-list">
                {featuredJobs.map((job) => (
                  <button
                    type="button"
                    key={job.id}
                    className="recommendation-row"
                    onClick={() => onSelectJob?.(job)}
                  >
                    <span className="company-mark">{initials(job.company)}</span>
                    <span>
                      <strong>{job.title}</strong>
                      <small>{job.company} · {job.location} · {badgeLabel(job.jobType)}</small>
                    </span>
                  </button>
                ))}
              </div>
            </div>

            <div id="jobs-anchor" />
            <section className="jobs-section jobs-section--pro">
              <div className="jobs-section__header">
                <div>
                  <h2 className="jobs-section__title">Jobs for your next move</h2>
                  {!loading && (
                    <p className="jobs-section__count">
                      {filteredJobs.length} position{filteredJobs.length !== 1 ? "s" : ""} found
                    </p>
                  )}
                </div>
                <button type="button" className="btn btn--outline" onClick={loadJobs} disabled={loading}>
                  {loading ? "Refreshing" : "Refresh jobs"}
                </button>
              </div>

              <Filters
                filterType={filterType}
                setFilterType={setFilterType}
                activeCategory={activeCategory}
                setActiveCategory={typeof setActiveCategory === "function" ? setActiveCategory : () => {}}
              />

              {loading && <Loader />}

              {!loading && error && (
                <div className="jobs-grid">
                  <Error message={error} onRetry={loadJobs} />
                </div>
              )}

              {!loading && !error && (
                <JobList
                  jobs={filteredJobs}
                  savedIds={savedIds}
                  onSave={onSave}
                  onSelect={onSelectJob}
                />
              )}
            </section>
          </main>

          <aside className="pro-rightbar">
            <div className="side-card">
              <div className="side-card__title-row">
                <h3>Hiring pulse</h3>
                <span>Live</span>
              </div>
              <ul className="pulse-list">
                {HIRING_UPDATES.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>

            <div className="side-card">
              <h3>Companies to follow</h3>
              <div className="company-list">
                {companies.map((job) => (
                  <button type="button" key={job.company} onClick={() => {
                    setSearchTerm?.(job.company);
                    document.getElementById("jobs-anchor")?.scrollIntoView({ behavior: "smooth" });
                  }}>
                    <span className="company-mark">{initials(job.company)}</span>
                    <span>
                      <strong>{job.company}</strong>
                      <small>{job.location || "Remote"} hiring</small>
                    </span>
                  </button>
                ))}
              </div>
            </div>

            <div className="side-card side-card--api">
              <h3>Developer access</h3>
              <p>Create backend-owned API keys for integrations and dashboards.</p>
              <button type="button" className="btn btn--outline" onClick={() => onNavigate?.("api-keys")}>
                Manage API keys
              </button>
            </div>
          </aside>
        </div>
      </section>
    </div>
  );
}

export default Home;
