import type {
  AnalyticsSummary,
  Job,
  RankedCandidate,
  Resume,
  ScoreBucket,
  Screening,
  ScreeningReport,
  SkillCount,
  SkillGap,
} from "./types";

const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const API = `${BASE}/api`;

async function http<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API}${path}`, {
    ...init,
    headers: {
      Accept: "application/json",
      ...(init?.body && !(init.body instanceof FormData)
        ? { "Content-Type": "application/json" }
        : {}),
      ...(init?.headers || {}),
    },
    cache: "no-store",
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`API ${res.status}: ${text || res.statusText}`);
  }
  if (res.status === 204) return undefined as unknown as T;
  return (await res.json()) as T;
}

export const api = {
  // Health
  health: () => http<{ status: string; version: string }>("/health"),

  // Jobs
  listJobs: () => http<Job[]>("/jobs"),
  getJob: (id: number) => http<Job>(`/jobs/${id}`),
  createJob: (payload: Omit<Job, "id" | "created_at">) =>
    http<Job>("/jobs", { method: "POST", body: JSON.stringify(payload) }),
  deleteJob: (id: number) => http<void>(`/jobs/${id}`, { method: "DELETE" }),

  // Resumes
  listResumes: () => http<Resume[]>("/resumes"),
  getResume: (id: number) => http<Resume>(`/resumes/${id}`),
  uploadResumes: (files: File[]) => {
    const fd = new FormData();
    files.forEach((f) => fd.append("files", f));
    return http<Resume[]>("/resumes/upload", { method: "POST", body: fd });
  },
  deleteResume: (id: number) => http<void>(`/resumes/${id}`, { method: "DELETE" }),

  // Screening
  runScreen: (jobId: number, resumeIds?: number[]) =>
    http<Screening[]>("/screen/run", {
      method: "POST",
      body: JSON.stringify({ job_id: jobId, resume_ids: resumeIds }),
    }),
  rankedFor: (jobId: number) =>
    http<RankedCandidate[]>(`/screen/job/${jobId}/ranked`),
  report: (screeningId: number) =>
    http<ScreeningReport>(`/screen/${screeningId}/report`),
  reportPdfUrl: (screeningId: number) =>
    `${API}/screen/${screeningId}/report.pdf`,

  // Analytics
  summary: () => http<AnalyticsSummary>("/analytics/summary"),
  scoreDist: () => http<ScoreBucket[]>("/analytics/score-distribution"),
  topSkills: (limit = 15) =>
    http<SkillCount[]>(`/analytics/top-skills?limit=${limit}`),
  skillGap: (jobId: number) =>
    http<SkillGap>(`/analytics/skill-gap/${jobId}`),
};
