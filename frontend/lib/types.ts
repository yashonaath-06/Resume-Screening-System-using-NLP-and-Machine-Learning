export interface Job {
  id: number;
  title: string;
  company: string;
  description: string;
  required_skills: string[];
  min_experience_years: number;
  education_level: string;
  created_at: string;
}

export interface Resume {
  id: number;
  candidate_name: string;
  email: string;
  phone: string;
  file_name: string;
  file_type: string;
  skills: string[];
  education: string[];
  experience_years: number;
  keywords: string[];
  entities: Record<string, string[]>;
  created_at: string;
}

export interface Screening {
  id: number;
  resume_id: number;
  job_id: number;
  ats_score: number;
  similarity: number;
  skill_match: number;
  keyword_match: number;
  experience_match: number;
  education_match: number;
  matched_skills: string[];
  missing_skills: string[];
  created_at: string;
}

export interface RankedCandidate {
  screening_id: number;
  resume_id: number;
  candidate_name: string;
  email: string;
  ats_score: number;
  similarity: number;
  matched_skills: string[];
  missing_skills: string[];
  rank: number;
}

export interface ScreeningReport {
  screening: Screening;
  resume: Resume;
  job: Job;
  report: {
    generated_at: string;
    candidate: Record<string, unknown>;
    job: Record<string, unknown>;
    scores: Record<string, number>;
    weights: Record<string, number>;
    matched_skills: string[];
    missing_skills: string[];
    verdict: string;
    recommendations: string[];
  };
}

export interface AnalyticsSummary {
  resumes: number;
  jobs: number;
  screenings: number;
  avg_ats_score: number;
}

export interface ScoreBucket {
  bucket: string;
  count: number;
}

export interface SkillCount {
  skill: string;
  count: number;
}

export interface SkillGap {
  job_id: number;
  total_screenings: number;
  gaps: { skill: string; candidates_missing: number }[];
}
