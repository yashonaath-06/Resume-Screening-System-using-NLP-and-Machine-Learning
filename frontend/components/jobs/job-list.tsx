"use client";
import * as React from "react";
import Link from "next/link";
import { Briefcase, Trash2, Play, Eye } from "lucide-react";
import { toast } from "sonner";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";
import type { Job } from "@/lib/types";

interface Props {
  jobs: Job[];
  onChange: () => void;
}

export function JobList({ jobs, onChange }: Props) {
  const [running, setRunning] = React.useState<number | null>(null);

  const handleScreen = async (jobId: number) => {
    setRunning(jobId);
    try {
      const res = await api.runScreen(jobId);
      toast.success(`Screened ${res.length} resume(s)`);
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setRunning(null);
    }
  };

  const handleDelete = async (jobId: number) => {
    if (!confirm("Delete this job and its screenings?")) return;
    try {
      await api.deleteJob(jobId);
      toast.success("Job deleted");
      onChange();
    } catch (e) {
      toast.error((e as Error).message);
    }
  };

  if (!jobs.length) {
    return (
      <Card>
        <CardContent className="py-10 text-center text-muted-foreground">
          No jobs yet. Create your first job description above.
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      {jobs.map((j) => (
        <Card key={j.id}>
          <CardHeader>
            <div className="flex items-start justify-between gap-2">
              <div>
                <CardTitle className="text-base flex items-center gap-2">
                  <Briefcase className="h-4 w-4 text-primary" />
                  {j.title}
                </CardTitle>
                <p className="text-xs text-muted-foreground mt-1">
                  {j.company || "—"} · {formatDate(j.created_at)}
                </p>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="secondary">{j.min_experience_years}+ yrs</Badge>
                {j.education_level ? (
                  <Badge variant="outline">{j.education_level}</Badge>
                ) : null}
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-3">
            <p className="text-sm text-muted-foreground line-clamp-3">
              {j.description}
            </p>
            <div className="flex flex-wrap gap-1">
              {j.required_skills.slice(0, 8).map((s) => (
                <Badge key={s} variant="outline">
                  {s}
                </Badge>
              ))}
              {j.required_skills.length > 8 ? (
                <Badge variant="outline">
                  +{j.required_skills.length - 8} more
                </Badge>
              ) : null}
            </div>
            <div className="flex items-center gap-2 pt-2">
              <Button
                size="sm"
                onClick={() => handleScreen(j.id)}
                disabled={running === j.id}
              >
                <Play className="h-3.5 w-3.5" />
                {running === j.id ? "Screening..." : "Screen all resumes"}
              </Button>
              <Link href={`/jobs/${j.id}`}>
                <Button size="sm" variant="outline">
                  <Eye className="h-3.5 w-3.5" />
                  View ranked
                </Button>
              </Link>
              <Button
                size="sm"
                variant="ghost"
                className="ml-auto text-rose-500 hover:text-rose-600"
                onClick={() => handleDelete(j.id)}
                aria-label="Delete job"
              >
                <Trash2 className="h-3.5 w-3.5" />
              </Button>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
