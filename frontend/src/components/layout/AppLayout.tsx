import { NavLink, Outlet } from "react-router-dom";
import {
  Activity, ArrowUpRight, BookOpenCheck, ChartNoAxesCombined, FileStack,
  GitCompareArrows, ScanSearch, ShieldCheck, Sparkles,
} from "lucide-react";
import { isDemoMode } from "../../services/api";

const navItems = [
  { to: "/documents", label: "Documents", icon: FileStack, description: "Upload & processing" },
  { to: "/explore", label: "Explore", icon: ScanSearch, description: "Search and verify" },
  { to: "/insights", label: "Insights", icon: ChartNoAxesCombined, description: "Aggregate patterns" },
  { to: "/compare", label: "Compare", icon: GitCompareArrows, description: "Review versions" },
  { to: "/review", label: "Review queue", icon: BookOpenCheck, description: "Resolve uncertainty" },
];

export default function AppLayout() {
  const demo = isDemoMode();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <NavLink to="/documents" className="brand" aria-label="RollLens AI home">
          <span className="brand-mark"><ScanSearch size={22} strokeWidth={2.2} /></span>
          <span className="brand-copy">
            <strong>RollLens<span> AI</span></strong>
            <small>THE EVIDENCE DESK</small>
          </span>
        </NavLink>

        <div className="workspace-label">WORKSPACE</div>
        <nav className="primary-nav" aria-label="Main navigation">
          {navItems.map(({ to, label, icon: Icon, description }) => (
            <NavLink key={to} to={to} className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}>
              <span className="nav-icon"><Icon size={18} /></span>
              <span className="nav-copy">
                <span>{label}</span>
                <small>{description}</small>
              </span>
              {to === "/documents" && <ArrowUpRight className="nav-arrow" size={14} />}
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="privacy-card">
            <span className="privacy-icon"><ShieldCheck size={17} /></span>
            <div>
              <strong>Evidence before inference</strong>
              <p>Every result should lead back to its source.</p>
            </div>
          </div>
          <div className="sidebar-foot">
            <span className={`status-dot ${demo ? "demo" : "live"}`} />
            <span>{demo ? "Sample workspace" : "Connected workspace"}</span>
            <span className="sidebar-version">v0.1</span>
          </div>
        </div>
      </aside>

      <div className="main-column">
        <header className="topbar">
          <div className="breadcrumb">
            <span>RollLens AI</span><span className="crumb-slash">/</span><strong>Research workspace</strong>
          </div>
          <div className="topbar-right">
            <span className={`mode-pill ${demo ? "mode-demo" : "mode-live"}`}>
              <span className="status-dot" />{demo ? "DEMO MODE" : "API MODE"}
            </span>
            <span className="topbar-divider" />
            <div className="avatar" aria-label="Demo researcher">DR</div>
          </div>
        </header>

        {demo && (
          <div className="demo-banner" role="status">
            <Sparkles size={15} />
            <span><strong>Demo workspace</strong> — sample data and simulated uploads are clearly labeled.</span>
            <span className="demo-banner-end"><Activity size={14} /> No live AI required</span>
          </div>
        )}

        <main className="page-content">
          <Outlet />
        </main>
        <footer className="app-footer">
          <span>RollLens AI <span className="footer-dot">·</span> Evidence-first civic research</span>
          <span>Sample records are illustrative, not official electoral data.</span>
        </footer>
      </div>
    </div>
  );
}
