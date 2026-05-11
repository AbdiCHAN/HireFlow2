# HireFlow

HireFlow is a job search and hiring web application built with React and a Node.js/Express backend.

It helps users browse jobs, search for jobs, filter jobs by category, view job details, and save jobs they like.

---

## Repository Description

This repository contains the full source code for HireFlow. It includes the React frontend, reusable components, styling files, and a backend API using Express. The backend provides job data to the frontend through API routes such as `/api/jobs`.

---

## Purpose of the Project

The purpose of HireFlow is to make job searching easier, faster, and more organized.

Users can:

- View available jobs
- Search for jobs
- Filter jobs by category
- View full job details
- Save jobs
- Visit pages like About, Categories, Candidates, News, Post Job, and CV Post

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

- Backend API setup
- Express server setup
- API routes
- Fetch logic
- App state management
- Loading and error handling
- Main app logic

**Files**

- `backend/server.js`
- `backend/services/api.js`
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
- Backend API for job data

---

## Technologies Used

- React
- JavaScript
- Vite
- CSS
- Node.js
- Express.js
- CORS
- Git
- GitHub

---

## Folder Structure

```txt
HIREFLOW/
│
├── backend/
│   ├── server.js
│   └── services/
│       └── api.js
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
│   ├── styles/
│   │   └── main.css
│   │
│   ├── App.css
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
│
├── .github/
│   └── workflows/
│       └── deploy.yml
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

### `backend/server.js`

This is the backend server file created by Abdirahman Cabdi.

It uses Express.js to run the backend API.

It includes routes such as:

```txt
GET /
GET /api/jobs
GET /api/jobs/categories
GET /api/jobs/:id
```

These routes provide job data to the frontend.

---

### `backend/services/api.js`

This file is used for backend API/job data logic if the project separates services from the main server file.

---

## Backend API Routes

### Test Backend

```txt
http://localhost:5000
```

Returns a message that the HireFlow backend is running.

---

### Get All Jobs

```txt
http://localhost:5000/api/jobs
```

Returns all available jobs.

---

### Search Jobs

```txt
http://localhost:5000/api/jobs?search=frontend
```

Returns jobs matching the search keyword.

---

### Filter Jobs by Category

```txt
http://localhost:5000/api/jobs?category=Engineering
```

Returns jobs from the selected category.

---

### Filter Jobs by Type

```txt
http://localhost:5000/api/jobs?type=Full-time
```

Returns jobs matching the selected job type.

---

### Get Categories

```txt
http://localhost:5000/api/jobs/categories
```

Returns all job categories.

---

### Get Single Job

```txt
http://localhost:5000/api/jobs/1
```

Returns one job by ID.

---

## How the Frontend and Backend Work Together

The frontend runs on:

```txt
http://localhost:5173/HireFlow/
```

The backend runs on:

```txt
http://localhost:5000
```

The frontend sends requests to the backend API.

Flow:

```txt
User searches or filters jobs
        ↓
React frontend updates state
        ↓
Frontend calls backend API
        ↓
Express backend returns job data
        ↓
Frontend displays the jobs
```

---

## How to Run the Project

### 1. Clone the Repository

```bash
git clone <repository-url>
```

### 2. Open the Project Folder

```bash
cd HireFlow
```

### 3. Install Dependencies

```bash
npm install
```

### 4. Run Frontend and Backend Together

```bash
npm run dev
```

This starts:

- Vite frontend
- Express backend server

---

## Development URLs

Frontend:

```txt
http://localhost:5173/HireFlow/
```

Backend:

```txt
http://localhost:5000
```

Backend jobs API:

```txt
http://localhost:5000/api/jobs
```

---

## How to Use HireFlow

1. Open the website.
2. Browse the available jobs.
3. Use the search bar to search for a job.
4. Use the filters to choose a category.
5. Click on a job card to view full details.
6. Click the save icon to save a job.
7. Use the navbar to move between pages.

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

- `JobList.jsx`
- `JobCard.jsx`

---

### `ui-ux-interaction`

Used for interaction and UX work.

Files:

- `SearchBar.jsx`
- `Filters.jsx`
- `Loader.jsx`
- `Error.jsx`

---

### `feature/ui-navbar`

Used for frontend layout and navbar work.

Files:

- `Navbar.jsx`
- `Home.jsx`
- CSS files

---

### `feature/api-fetch-logic`

Used for Abdirahman Cabdi’s API and app logic work.

Files:

- `backend/server.js`
- `backend/services/api.js`
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
git commit -m "Add backend server and API routes"
```

### 7. Push branch

```bash
git push origin feature/api-fetch-logic
```

### 8. Create a pull request

Create a pull request from your branch into `main`.

Example:

```txt
feature/api-fetch-logic → main
```

---

## Example Commit Messages

```txt
Add backend server
Add jobs API routes
Fix app logic
Add loader component
Improve navbar styling
Add job cards
Update README
```

---

## Project Summary

HireFlow is a React and Node.js job search platform.

It allows users to:

- Search jobs
- Filter jobs
- View job details
- Save jobs
- Navigate career pages

The project is divided into team roles so each member works on a clear part of the system.

Abdirahman Cabdi is responsible for the backend API and main app logic, including `backend/server.js` and `src/App.jsx`.
