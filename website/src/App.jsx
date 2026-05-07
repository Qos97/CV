import { Routes, Route, NavLink, useLocation } from 'react-router-dom'
import { useState, useEffect, lazy, Suspense } from 'react'
import { LanguageProvider, useLang } from './LanguageContext'
import content from './content.json'
import './App.css'

const Home          = lazy(() => import('./pages/Home'))
const About         = lazy(() => import('./pages/About'))
const Experience    = lazy(() => import('./pages/Experience'))
const Skills        = lazy(() => import('./pages/Skills'))
const Projects      = lazy(() => import('./pages/Projects'))
const Certifications = lazy(() => import('./pages/Certifications'))
const Contact       = lazy(() => import('./pages/Contact'))

function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)
  const { lang, setLang } = useLang()
  const location = useLocation()
  const labels = content[lang].nav

  const NAV_LINKS = [
    { to: '/about',          label: labels.about },
    { to: '/experience',     label: labels.experience },
    { to: '/skills',         label: labels.skills },
    { to: '/projects',       label: labels.projects },
    { to: '/certifications', label: labels.certifications },
    { to: '/contact',        label: labels.contact },
  ]

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 10)
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  useEffect(() => { setMenuOpen(false) }, [location])

  return (
    <header className={`navbar${scrolled ? ' navbar--scrolled' : ''}`}>
      <div className="container navbar__inner">
        <NavLink to="/" className="navbar__logo">
          <span className="navbar__logo-initials">FF</span>
          <span className="navbar__logo-name">Filipe Fernandes</span>
        </NavLink>

        <nav className={`navbar__nav${menuOpen ? ' navbar__nav--open' : ''}`}>
          {NAV_LINKS.map(l => (
            <NavLink
              key={l.to}
              to={l.to}
              className={({ isActive }) => `navbar__link${isActive ? ' navbar__link--active' : ''}`}
            >
              {l.label}
            </NavLink>
          ))}
          <a
            href={`${import.meta.env.BASE_URL}${lang === 'en' ? 'CV_Filipe_Fernandes_EN.pdf' : 'CV_Filipe_Fernandes_PT.pdf'}`}
            download
            className="btn btn-primary navbar__cta"
          >
            {labels.download}
          </a>
          <div className="lang-toggle">
            <button
              className={`lang-toggle__btn${lang === 'en' ? ' lang-toggle__btn--active' : ''}`}
              onClick={() => setLang('en')}
            >EN</button>
            <span className="lang-toggle__sep">|</span>
            <button
              className={`lang-toggle__btn${lang === 'pt' ? ' lang-toggle__btn--active' : ''}`}
              onClick={() => setLang('pt')}
            >PT</button>
          </div>
        </nav>

        <button
          className={`navbar__burger${menuOpen ? ' navbar__burger--open' : ''}`}
          onClick={() => setMenuOpen(v => !v)}
          aria-label="Toggle menu"
        >
          <span /><span /><span />
        </button>
      </div>
    </header>
  )
}

function Footer() {
  return (
    <footer className="footer">
      <div className="container footer__inner">
        <span>© {new Date().getFullYear()} Filipe Fernandes</span>
        <span className="footer__links">
          <a href="https://linkedin.com/in/fgfernandes97" target="_blank" rel="noreferrer">LinkedIn</a>
        </span>
      </div>
    </footer>
  )
}

export default function App() {
  return (
    <LanguageProvider>
      <Navbar />
      <main style={{ paddingTop: 'var(--nav-h)' }}>
        <Suspense fallback={<div style={{ padding: '80px 0', textAlign: 'center' }} />}>
          <Routes>
            <Route path="/"               element={<Home />} />
            <Route path="/about"          element={<About />} />
            <Route path="/experience"     element={<Experience />} />
            <Route path="/skills"         element={<Skills />} />
            <Route path="/projects"       element={<Projects />} />
            <Route path="/certifications" element={<Certifications />} />
            <Route path="/contact"        element={<Contact />} />
          </Routes>
        </Suspense>
      </main>
      <Footer />
    </LanguageProvider>
  )
}
