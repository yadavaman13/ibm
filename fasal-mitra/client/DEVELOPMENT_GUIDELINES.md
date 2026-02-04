# FasalMitra Client Development Guidelines

**Version:** 1.0.0  
**Last Updated:** February 4, 2026

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Code Standards](#code-standards)
4. [Styling Guidelines](#styling-guidelines)
5. [Component Structure](#component-structure)
6. [State Management](#state-management)
7. [API Integration](#api-integration)
8. [Accessibility](#accessibility)
9. [Performance](#performance)
10. [Git Workflow](#git-workflow)

---

## Project Overview

FasalMitra is a Smart Farming Assistant built with React + Vite + Tailwind CSS. The application provides AI-powered agricultural advisory services to farmers.

**Core Features:**
- 🌾 Yield Prediction (ML-based)
- 🌤️ Weather Forecasting
- 🧪 Soil Analysis
- 🦠 Disease Detection (AI image-based)
- 📊 Gap Analysis
- 💬 AI Chatbot

---

## Tech Stack

- **Framework:** React 19.1.0
- **Build Tool:** Vite 7.0.4
- **Styling:** Tailwind CSS 4.1.18
- **Icons:** Lucide React
- **Routing:** React Router DOM
- **Backend:** FastAPI (separate server)

---

## Code Standards

### File Organization

```
src/
├── assets/            # Images, icons, fonts
├── components/        # Reusable UI components
├── pages/             # Route-level components
├── hooks/             # Custom React hooks (future)
├── services/          # API calls (future)
├── styles/            # CSS files
│   ├── navbar.css
│   ├── feature-card.css
│   ├── dashboard.css
│   └── pages.css
├── App.jsx
├── main.jsx
└── index.css
```

### Naming Conventions

**Files:**
- Components: `PascalCase.jsx` (e.g., `FeatureCard.jsx`)
- CSS files: `kebab-case.css` (e.g., `feature-card.css`)
- Pages: `PascalCase.jsx` (e.g., `Dashboard.jsx`)

**Variables/Functions:**
- camelCase for variables and functions
- PascalCase for React components
- UPPER_SNAKE_CASE for constants

**CSS Classes:**
- `kebab-case` for class names (e.g., `feature-card-icon`)
- Use semantic naming (describe purpose, not appearance)

---

## Styling Guidelines

### ⚠️ CRITICAL: Use CSS Variables, NOT Inline Styles

**❌ NEVER do this:**
```jsx
<div style={{ backgroundColor: '#99BC85' }}>
```

**✅ ALWAYS do this:**
```jsx
<div className="dashboard-hero-title-accent">
```

### Theme System

All colors are defined in `src/index.css` as CSS variables:

```css
:root {
  /* Color Palette */
  --color-primary: #99BC85;           /* Sage green */
  --color-primary-light: #E4EFE7;     /* Light mint */
  --color-background: #FDFAF6;        /* Light cream */
  --color-surface: #FAF1E6;           /* Warm beige */
  
  /* Semantic Colors */
  --color-text-primary: #1f2937;
  --color-text-secondary: #6b7280;
  --color-border: #e5e7eb;
}
```

**Why?** 
- ✅ Easy theme switching (change 4 variables, entire app updates)
- ✅ Single source of truth
- ✅ Better maintainability
- ✅ Production-ready

### Tailwind vs Custom CSS

**Use Tailwind for:**
- Layout (flex, grid)
- Spacing, sizing
- Typography & colors
- Responsive design
- 80-90% of styling

```jsx
<div className="flex items-center gap-4 p-4 bg-white rounded-lg shadow">
```

**Use Custom CSS for:**
- Complex animations
- `::before` / `::after` pseudo-elements
- Keyframes
- Very long repeated utility chains
- Component-specific styles

**Custom CSS Files:**
- Create in `src/styles/` folder
- Name after component: `navbar.css`, `feature-card.css`
- Import in component: `import '../styles/navbar.css';`

### Responsive Design (Mobile-First)

**ALWAYS design mobile-first:**

```jsx
// ✅ Good - Mobile first
<div className="text-sm md:text-base lg:text-lg">

// ❌ Bad - Desktop first
<div className="text-lg md:text-base sm:text-sm">
```

**Breakpoints:**
- Default: Mobile (< 768px)
- `sm:` Tablet (≥ 768px)
- `md:` Desktop (≥ 1024px)
- `lg:` Large Desktop (≥ 1280px)

---

## Component Structure

### Component Best Practices

1. **Single Responsibility** - One component, one purpose
2. **Keep Small** - Max ~150 lines, split if larger
3. **Reusable** - Extract common patterns
4. **Stateless when possible** - Prefer functional components

### Component Template

```jsx
import React from 'react';
import { Icon } from 'lucide-react';
import '../styles/component-name.css';

const ComponentName = ({ prop1, prop2 }) => {
  return (
    <div className="component-container">
      {/* Component content */}
    </div>
  );
};

export default ComponentName;
```

### Props Guidelines

- Pass only what is needed
- Provide default values
- Use destructuring

```jsx
// ✅ Good
function Button({ label, variant = 'primary', onClick }) {
  return <button className={`btn-${variant}`} onClick={onClick}>{label}</button>;
}

// ❌ Bad
function Button(props) {
  return <button>{props.label}</button>;
}
```

---

## State Management

### Local State

Use `useState` for component-local state:

```jsx
const [isOpen, setIsOpen] = useState(false);
```

### Derived State

**❌ Don't store derived data:**
```js
const [fullName, setFullName] = useState(firstName + ' ' + lastName); // Bad
```

**✅ Compute on render:**
```js
const fullName = `${firstName} ${lastName}`; // Good
```

### Global State

- For global state (when needed), use Context API or Zustand
- **Don't use Redux unless absolutely necessary**
- Keep state as local as possible

---

## API Integration

### API Base URL

Backend runs at: `http://localhost:8000`

### API Service Pattern (Future)

Create `src/services/api.js`:

```js
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export const api = {
  async predictYield(data) {
    const response = await fetch(`${API_BASE_URL}/yield/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }
};
```

### Error Handling

Always handle errors gracefully:

```jsx
try {
  const result = await api.predictYield(formData);
  // Handle success
} catch (error) {
  console.error('Prediction failed:', error);
  // Show user-friendly error message
}
```

**Reference:** See `fasal-mitra/server/API_DOCUMENTATION.md` for complete API docs.

---

## Accessibility

### ⚠️ NON-NEGOTIABLE Requirements

1. **Semantic HTML**
   ```jsx
   // ✅ Good
   <button>Click me</button>
   
   // ❌ Bad
   <div onClick={handleClick}>Click me</div>
   ```

2. **Alt Text for Images**
   ```jsx
   <img src="crop.jpg" alt="Wheat crop in field" />
   ```

3. **ARIA Labels**
   ```jsx
   <button aria-label="Close modal">
     <X className="w-6 h-6" />
   </button>
   ```

4. **Keyboard Navigation**
   - All interactive elements must be keyboard accessible
   - Test with Tab, Enter, Escape keys

5. **Focus Styles**
   - Never remove focus outlines without replacement
   - Use `focus:outline-none focus:ring-2` pattern

---

## Performance

### Required Practices

1. **Lazy Load Routes**
   ```jsx
   const Dashboard = lazy(() => import('./pages/Dashboard'));
   ```

2. **Optimize Images**
   - Use WebP format
   - Compress before adding to repo
   - Use appropriate sizes

3. **Memoization (when needed)**
   ```jsx
   const MemoizedComponent = memo(ExpensiveComponent);
   ```

4. **Avoid Unnecessary Re-renders**
   - Don't create functions/objects in render
   - Use `useCallback` for event handlers in lists

---

## Git Workflow

### Branch Naming

- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `refactor/what-changed` - Code improvements
- `docs/what-updated` - Documentation

### Commit Messages

Follow conventional commits:

```
feat: add yield prediction form
fix: resolve navbar mobile menu bug
refactor: extract API calls to service layer
docs: update API integration guide
style: apply custom color theme
```

### Pull Request Rules

1. **No direct commits to `main`**
2. Small, focused PRs (one feature/fix per PR)
3. Include screenshots for UI changes
4. Test locally before creating PR
5. Get at least one review before merging

---

## Code Quality

### ESLint & Prettier

**Run before committing:**
```bash
npm run lint
```

### No Console Logs in Production

```js
// ❌ Bad
console.log('User data:', userData);

// ✅ Good (development only)
if (import.meta.env.DEV) {
  console.log('Debug:', data);
}
```

### Clear Naming

```js
// ❌ Bad
const d = fetchData();
const x = users.map(u => u.n);

// ✅ Good
const userProfileResponse = fetchUserProfile();
const userNames = users.map(user => user.name);
```

---

## Design System

### Color Usage

**Primary Actions:** Use `--color-primary` (#99BC85)
- Primary buttons
- Active states
- Important text highlights

**Backgrounds:**
- Page background: `--color-background` (#FDFAF6)
- Card/surface: `white` or `--color-surface` (#FAF1E6)
- Hover states: `--color-primary-light` (#E4EFE7)

**Text:**
- Primary text: `--color-text-primary` or `text-gray-800`
- Secondary text: `--color-text-secondary` or `text-gray-600`

### Typography Scale

```jsx
// Headings
<h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold">
<h2 className="text-2xl font-bold">
<h3 className="text-xl font-semibold">

// Body
<p className="text-base">
<p className="text-sm text-gray-600">
```

### Spacing

Use consistent spacing:
- `gap-4` for card grids
- `mb-8` for section spacing
- `py-8 sm:py-12` for vertical padding (responsive)

---

## Important Documents to Read

### Before Starting Development:

1. **`fasal-mitra/server/API_DOCUMENTATION.md`** - Complete API reference
2. **`fasal-mitra/START_GUIDE.md`** - Project setup guide
3. **`DEVELOPMENT_GUIDELINES.md`** (this file) - Frontend standards

### External Resources:

- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Lucide React Icons](https://lucide.dev/)
- [React Router Docs](https://reactrouter.com/)

---

## Design Principles

### Keep It Simple

> "Don't overwhelm farmers with information. Show only what's needed."

- Clean, minimal design
- Prioritize important data
- Use visual hierarchy
- Progressive disclosure (hide advanced options)

### Mobile-First Always

Farmers primarily use mobile devices. Design for mobile, enhance for desktop.

### Accessibility First

Agricultural workers may have varying tech literacy. Make it intuitive and easy to understand.

---

## Common Mistakes to Avoid

### ❌ Don't:
1. Use inline styles for colors
2. Hardcode API URLs
3. Create giant components (>200 lines)
4. Ignore mobile responsiveness
5. Skip accessibility attributes
6. Commit `console.log` statements
7. Use non-semantic HTML (`<div onClick>` instead of `<button>`)
8. Store derived state in `useState`

### ✅ Do:
1. Use CSS variables for theming
2. Use environment variables for config
3. Split large components into smaller ones
4. Design mobile-first
5. Add ARIA labels and alt text
6. Clean up debugging code
7. Use semantic HTML
8. Compute derived data on render

---

## Professional Mindset

> **"Make it work" → Beginner**  
> **"Make it clean" → Intermediate**  
> **"Make it scalable" → Professional**

Always ask:
- ✅ Can this scale?
- ✅ Can another developer understand this?
- ✅ Will this be easy to change later?
- ✅ Does this follow our guidelines?

---

## Getting Help

### When Stuck:

1. Check `API_DOCUMENTATION.md` for API issues
2. Check this file for coding standards
3. Check `START_GUIDE.md` for setup issues
4. Ask team lead for architecture decisions

### Before Asking for Help:

1. Read error messages carefully
2. Check browser console
3. Review relevant documentation
4. Try debugging with console.log
5. Search for similar issues

---

## Quick Reference

### Start Development Server
```bash
npm run dev
```

### Build for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

### Lint Code
```bash
npm run lint
```

---

## Version History

- **v1.0.0** (Feb 4, 2026) - Initial guidelines
  - Established CSS variable system
  - Mobile-first responsive design
  - Component structure guidelines
  - API integration patterns

---

**Remember: Clean code is not just about making it work. It's about making it maintainable, scalable, and understandable for the entire team.**

Happy Coding! 🚀🌾
