"use client";
import * as React from "react";
import { toast } from "sonner";
import { ResumeList } from "@/components/candidates/resume-list";
import { api } from "@/lib/api";
import type { Resume } from "@/lib/types";

export default function CandidatesPage() {
  const [resumes, setResumes] = React.useState<Resume[]>([]);

  const refresh = React.useCallback(async () => {
    try {
      setResumes(await api.listResumes());
    } catch (e) {
      toast.error((e as Error).message);
    }
  }, []);

  React.useEffect(() => {
    refresh();
  }, [refresh]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Candidates</h1>
        <p className="text-sm text-muted-foreground">
          All parsed resumes with extracted skills, experience, and contact info.
        </p>
      </div>
      <ResumeList resumes={resumes} onChange={refresh} />
    </div>
  );
}
