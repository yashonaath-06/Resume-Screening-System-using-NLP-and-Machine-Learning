"use client";
import * as React from "react";
import { useParams } from "next/navigation";
import { toast } from "sonner";
import { Loader2, Play } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CandidateTable } from "@/components/candidates/candidate-table";
import { api } from "@/lib/api";
import type { Job, RankedCandidate, SkillGap } from "@/lib/types";

export default function JobDetailPage() {
  const params = useParams<{ id: string }>();
  const jobId = Number(params?.id);

  const [job, setJob] = React.useState<Job | null>(null);
  const [ranked, setRanked] = React.useState<RankedCandidate[]>([]);
  const [gap, setGap] = React.useState<SkillGap | null>(null);
  const [running, setRunning] = React.useState(false);

  const refresh = React.useCallback(async () => {
    try {
      const [j, r, g] = await Promise.all([
        api.getJob(jobId),
        api.rankedFor(jobId),
        api.skillGap(jobId),
      ]);
      setJob(j);
      setRanked(r);
      setGap(g);
    } catch (e) {
      toast.error((e as Error).message);
    }
  }, [jobId]);

  React.useEffect(() => {
    if (Number.isFinite(jobId)) refresh();
  }, [jobId, refresh]);

  const runScreening = async () => {
    setRunning(true);
    try {
      const out = await api.runScreen(jobId);
      toast.success(`Screened ${out.length} resume(s)`);
      await refresh();
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setRunning(false);
    }
  };

  if (!job) {
    return (
      <div className="flex items-center gap-2 text-muted-foreground">
        <Loader2 className="h-4 w-4 animate-spin" />
        Loading job...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">{job.title}</h1>
          <p className="text-sm text-muted-foreground">
            {job.company || "—"} · Min {job.min_experience_years} yrs · Education:{" "}
            {job.education_level || "any"}
          </p>
        </div>
        <Button onClick={runScreening} disabled={running}>
          {running ? <Loader2 className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />}
          {running ? "Screening..." : "Screen all resumes"}
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Required skills</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-1">
          {job.required_skills.length ? (
            job.required_skills.map((s) => (
              <Badge key={s} variant="outline">{s}</Badge>
            ))
          ) : (
            <span className="text-sm text-muted-foreground">No skills set.</span>
          )}
        </CardContent>
      </Card>

      <CandidateTable rows={ranked} />

      {gap && gap.gaps.length ? (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">
              Aggregate skill gap ({gap.total_screenings} candidates)
            </CardTitle>
          </CardHeader>
          <CardContent className="flex flex-wrap gap-2">
            {gap.gaps.map((g) => (
              <Badge key={g.skill} variant="warn">
                {g.skill} · {g.candidates_missing}
              </Badge>
            ))}
          </CardContent>
        </Card>
      ) : null}
    </div>
  );
}
