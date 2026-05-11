export const LOGO_COLORS = [
  "#7c3aed",
  "#2563eb",
  "#06b6d4",
  "#10b981",
  "#f59e0b",
  "#ef4444",
];

export const DEMO_JOBS = [
  {
    id: 1,
    title: "iOS Developer",
    company: "NOORO",
    logo: "🧸",
    location: "USA",
    type: "Full-time",
    category: "Engineering",
    salary: "$60k-$130k (depending on experience)",
    description:
      "WHO ARE WE? At Nooro, we’re revolutionizing pain management for seniors. Our platform is transforming how older adults engage with care, support, and digital health tools.",
    tags: ["api", "backend", "git", "ios", "security"],
  },
  {
    id: 2,
    title: "Senior DevOps Engineer",
    company: "LEMON.IO",
    logo: "👁️",
    location: "Americas, Europe, Asia, Oceania",
    type: "Full-time",
    category: "Engineering",
    salary: "$80k-$150k",
    description:
      "Are you a talented Senior DevOps looking for a remote job that lets you show your skills and get decent compensation? Join a marketplace that connects engineers with global companies.",
    tags: [".Net", "android", "AWS", "azure", "C"],
  },
  {
    id: 3,
    title: "Frontend Developer",
    company: "HireFlow",
    logo: "⚛️",
    location: "Nairobi, Kenya",
    type: "Full-time",
    category: "Development",
    salary: "$40k-$90k",
    description:
      "Build responsive React interfaces and improve the user experience for a modern hiring platform.",
    tags: ["react", "javascript", "css", "vite"],
  },
  {
    id: 4,
    title: "UI/UX Designer",
    company: "DesignHub",
    logo: "🎨",
    location: "Remote",
    type: "Contract",
    category: "Design",
    salary: "$30k-$70k",
    description:
      "Create clean layouts, user flows, wireframes, and visual designs for web applications.",
    tags: ["figma", "ux", "ui", "design"],
  },
  {
    id: 5,
    title: "Marketing Specialist",
    company: "GrowthLab",
    logo: "📣",
    location: "Hybrid",
    type: "Part-time",
    category: "Marketing",
    salary: "$25k-$60k",
    description:
      "Support campaigns, content strategy, social media, and growth marketing experiments.",
    tags: ["seo", "content", "social", "ads"],
  },
  {
    id: 6,
    title: "Finance Assistant",
    company: "CapitalWorks",
    logo: "💼",
    location: "Nairobi, Kenya",
    type: "Full-time",
    category: "Finance",
    salary: "$35k-$75k",
    description:
      "Assist with finance operations, reporting, invoices, budgeting, and account management.",
    tags: ["finance", "excel", "reporting", "budget"],
  },
  {
    id: 7,
    title: "Product Manager",
    company: "NovaTech",
    logo: "🚀",
    location: "Remote",
    type: "Full-time",
    category: "Management",
    salary: "$70k-$140k",
    description:
      "Lead product planning, roadmap decisions, customer research, and team coordination.",
    tags: ["product", "strategy", "roadmap", "management"],
  },
  {
    id: 8,
    title: "Digital Content Creator",
    company: "MediaFlow",
    logo: "🎬",
    location: "Remote",
    type: "Contract",
    category: "Digital",
    salary: "$20k-$55k",
    description:
      "Create digital content for websites, campaigns, social media, and brand storytelling.",
    tags: ["content", "video", "digital", "brand"],
  },
];

export function normalizeType(type = "") {
  return String(type).toLowerCase().trim();
}

export function filterJobs(
  jobs = DEMO_JOBS,
  { search = "", category = "All", type = "All" } = {}
) {
  const normalizedSearch = String(search).toLowerCase().trim();
  const normalizedCategory = String(category).toLowerCase().trim();
  const normalizedType = String(type).toLowerCase().trim();

  return jobs.filter((job) => {
    const searchableText = [
      job.title,
      job.company,
      job.location,
      job.type,
      job.category,
      job.salary,
      job.description,
      ...(job.tags || []),
    ]
      .join(" ")
      .toLowerCase();

    const matchesSearch =
      !normalizedSearch || searchableText.includes(normalizedSearch);

    const matchesCategory =
      !normalizedCategory ||
      normalizedCategory === "all" ||
      job.category.toLowerCase() === normalizedCategory;

    const matchesType =
      !normalizedType ||
      normalizedType === "all" ||
      job.type.toLowerCase() === normalizedType;

    return matchesSearch && matchesCategory && matchesType;
  });
}

export async function fetchJobs(filters = {}) {
  try {
    const params = new URLSearchParams();

    if (filters.search) params.set("search", filters.search);
    if (filters.category) params.set("category", filters.category);
    if (filters.type) params.set("type", filters.type);

    const response = await fetch(`/api/jobs?${params.toString()}`);

    if (!response.ok) {
      throw new Error("Backend request failed");
    }

    const result = await response.json();
    return result.data || [];
  } catch {
    return filterJobs(DEMO_JOBS, filters);
  }
}

export async function fetchJobById(id) {
  try {
    const response = await fetch(`/api/jobs/${id}`);

    if (!response.ok) {
      throw new Error("Backend request failed");
    }

    const result = await response.json();
    return result.data;
  } catch {
    return DEMO_JOBS.find((job) => String(job.id) === String(id)) || null;
  }
}

export async function fetchCategories() {
  try {
    const response = await fetch("/api/jobs/categories");

    if (!response.ok) {
      throw new Error("Backend request failed");
    }

    const result = await response.json();
    return result.data || [];
  } catch {
    return ["All", ...new Set(DEMO_JOBS.map((job) => job.category))];
  }
}
