# HireFlow

HireFlow is a job search and hiring web application built with React and Vite.

It helps users browse jobs, search for jobs, filter jobs by category, view job details, and save jobs they like.

---

## Repository Description

This repository contains the source code for HireFlow. It includes the React frontend, reusable components, styling files, page logic, and frontend API helper logic used to fetch and display job listings.

The `backend/` folder currently exists as a placeholder only. It does not contain backend files yet.

---

## Purpose of the Project

The purpose of HireFlow is to make job searching easier, faster, and more organized.

Users can:

- View available jobs
- Search for jobs
- Filter jobs by category
- View full job details
- Save jobs
- Visit pages like About, Categories, Candidates, News, Job Post, and CV Post

---

## Team Members and Responsibilities

### 👨‍💻 Athanas – Frontend Lead

**Responsibilities**

- Navbar
- Home page layout
- Page design
- Basic styling
- Mobile responsiveness

**Files**

- `src/components/Navbar.jsx`
- `src/pages/Home.jsx`
- `src/styles/main.css`
- `src/App.css`
- `src/index.css`

---

### 👨‍💻 Abdirahman Cabdi – API & Logic Lead

**Responsibilities**

- Frontend API helper logic
- Fetch logic
- Job data handling
- App state management
- Loading and error handling
- Main app logic

**Files**

- `src/services/api.js`
- `src/App.jsx`

---

### 👨‍💻 Donald – Data Display Lead

**Responsibilities**

- Job cards
- Job list
- Displaying job information clearly

**Files**

- `src/components/JobList.jsx`
- `src/components/JobCard.jsx`

---

### 👨‍💻 Albert – Interaction & UX Lead

**Responsibilities**

- Search
- Filters
- Loader
- Error messages
- User interaction

**Files**

- `src/components/SearchBar.jsx`
- `src/components/Filters.jsx`
- `src/components/Loader.jsx`
- `src/components/Error.jsx`

---

## Main Features

- Browse available jobs
- Search jobs by keyword
- Filter jobs by category
- View job details
- Save jobs
- Navigate between different pages
- Loading and error states
- Frontend API helper for job data
- GitHub Pages deployment support

---

## Technologies Used

- React
- JavaScript
- Vite
- CSS
- Git
- GitHub
- GitHub Pages

---

## Folder Structure

```txt
HIREFLOW2/
│
├── backend/
│
├── public/
│
├── src/
│   ├── assets/
│   │   ├── hero.png
│   │   ├── react.svg
│   │   └── vite.svg
│   │
│   ├── components/
│   │   ├── Error.jsx
│   │   ├── Filters.jsx
│   │   ├── JobCard.jsx
│   │   ├── JobList.jsx
│   │   ├── Loader.jsx
│   │   ├── Navbar.jsx
│   │   └── SearchBar.jsx
│   │
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── InfoPages.jsx
│   │   └── JobDetails.jsx
│   │
│   ├── services/
│   │   └── api.js
│   │
│   ├── styles/
│   │   └── main.css
│   │
│   ├── App.css
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
│
├── .gitignore
├── index.html
├── package.json
├── package-lock.json
├── README.md
└── vite.config.js
```

---

## Important Files

### `src/main.jsx`

Starts the React app and connects it to `index.html`.

---

### `src/App.jsx`

Controls the main logic of the app.

It manages:

- Current page
- Selected job
- Saved jobs
- Search term
- Active category
- Navigation logic

---

### `src/pages/Home.jsx`

Displays the home page, search area, filters, and job listings.

---

### `src/pages/JobDetails.jsx`

Displays full information about a selected job.

---

### `src/pages/InfoPages.jsx`

Contains extra pages such as:

- About
- Categories
- Candidates
- News
- Post Job
- CV Post

---

### `src/services/api.js`

Contains the frontend job data and API helper logic.

This file helps the app:

- Fetch jobs
- Filter jobs
- Normalize job data
- Handle fallback demo jobs
- Open apply links

---

### `backend/`

This folder is currently empty.

It is kept as a placeholder for future backend work if the project later needs a real backend server, database, routes, or controllers.

---

## How the App Works

HireFlow currently works mainly as a frontend React application.

Flow:

```txt
User searches or filters jobs
        ↓
React frontend updates state
        ↓
src/services/api.js handles job data
        ↓
Jobs are displayed in JobList and JobCard
        ↓
User can view details or apply
```

---

## GitHub Pages Note

GitHub Pages only hosts frontend/static websites.

That means GitHub Pages can run:

- HTML
- CSS
- JavaScript
- React build files

GitHub Pages does not run a backend server.

For this project, the live GitHub Pages version uses frontend logic from:

```txt
src/services/api.js
```

---

## How to Run the Project Locally

### 1. Clone the Repository

```bash
git clone <repository-url>
```

### 2. Open the Project Folder

```bash
cd HireFlow2
```

### 3. Install Dependencies

```bash
npm install
```

### 4. Run the Project

```bash
npm run dev
```

### 5. Open the Local Website

```txt
http://localhost:5173/
```

---

## How to Build the Project

```bash
npm run build
```

This creates a production-ready version of the app inside the `dist/` folder.

---

## How to Deploy to GitHub Pages

Make sure GitHub Pages is set to:

```txt
Source: Deploy from a branch
Branch: gh-pages
Folder: / root
```

Then deploy with:

```bash
npm run deploy
```

After deployment, the live website should be available at:

```txt
https://abdichan.github.io/HireFlow2/
```

---

## How to Push Changes

After editing files, run:

```bash
git status
git add .
git commit -m "Update HireFlow"
git push origin main
```

Then redeploy:

```bash
npm run deploy
```

---

## How to Use HireFlow

1. Open the website.
2. Browse the available jobs.
3. Use the search bar to search for a job.
4. Use the filters to choose a category.
5. Click on a job card to view full details.
6. Click the save icon to save a job.
7. Click Apply to open the job application link.
8. Use the navbar to move between pages.

---

## Git Branches

The project uses different branches for different team members.

```txt
main
donald
ui-ux-interaction
feature/ui-navbar
feature/api-fetch-logic
```

---

## Branch Responsibilities

### `main`

Main stable branch. Only working code should be merged here.

---

### `donald`

Used for job display work.

Files:

- `src/components/JobList.jsx`
- `src/components/JobCard.jsx`

---

### `ui-ux-interaction`

Used for interaction and UX work.

Files:

- `src/components/SearchBar.jsx`
- `src/components/Filters.jsx`
- `src/components/Loader.jsx`
- `src/components/Error.jsx`

---

### `feature/ui-navbar`

Used for frontend layout and navbar work.

Files:

- `src/components/Navbar.jsx`
- `src/pages/Home.jsx`
- CSS files

---

### `feature/api-fetch-logic`

Used for Abdirahman Cabdi’s API and app logic work.

Files:

- `src/services/api.js`
- `src/App.jsx`

---

## Git Flow

### 1. Start from main

```bash
git checkout main
git pull origin main
```

### 2. Switch to your branch

Example:

```bash
git checkout feature/api-fetch-logic
```

### 3. Make your changes

Work on the files assigned to your role.

### 4. Check changes

```bash
git status
```

### 5. Add changes

```bash
git add .
```

### 6. Commit changes

```bash
git commit -m "Fix app logic"
```

### 7. Push branch

```bash
git push origin feature/api-fetch-logic
```

### 8. Create a Pull Request

Create a pull request from your branch into `main`.

Example:

```txt
feature/api-fetch-logic → main
```

---

## Example Commit Messages

```txt
Fix app logic
Update job cards
Improve navbar styling
Add loader component
Fix search filtering
Update README
Improve mobile responsiveness
Deploy to GitHub Pages
```

---

## Project Summary

HireFlow is a React and Vite job search platform.

It allows users to:

- Search jobs
- Filter jobs
- View job details
- Save jobs
- Apply for jobs
- Navigate career pages

The project is divided into team roles so each member works on a clear part of the system.

The `backend/` folder is currently empty and is only kept for future backend development.