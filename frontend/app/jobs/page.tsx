"use client";
import * as React from "react";
import { toast } from "sonner";
import { JobForm } from "@/components/jobs/job-form";
import { JobList } from "@/components/jobs/job-list";
import { api } from "@/lib/api";
import type { Job } from "@/lib/types";

export default function JobsPage() {
  const [jobs, setJobs] = React.useState<Job[]>([]);

  const refresh = React.useCallback(async () => {
    try {
      setJobs(await api.listJobs());
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
        <h1 className="text-2xl font-bold tracking-tight">Jobs</h1>
        <p className="text-sm text-muted-foreground">
          Define the role and required skills. Then screen all uploaded resumes against it.
        </p>
      </div>

      <JobForm onCreated={refresh} />

      <div>
        <h2 className="text-lg font-semibold mb-3">All jobs</h2>
        <JobList jobs={jobs} onChange={refresh} />
      </div>
    </div>
  );
}
