"use client";
import * as React from "react";
import Link from "next/link";
import { toast } from "sonner";

import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";
import type { Job, RankedCandidate } from "@/lib/types";

export default function ReportsHubPage() {
  const [jobs, setJobs] = React.useState<Job[]>([]);
  const [selected, setSelected] = React.useState<number | null>(null);
  const [rows, setRows] = React.useState<RankedCandidate[]>([]);

  React.useEffect(() => {
    (async () => {
      try {
        const j = await api.listJobs();
        setJobs(j);
        if (j[0]) setSelected(j[0].id);
      } catch (e) {
        toast.error((e as Error).message);
      }
    })();
  }, []);

  React.useEffect(() => {
    if (!selected) return;
    (async () => {
      try {
        setRows(await api.rankedFor(selected));
      } catch (e) {
        toast.error((e as Error).message);
      }
    })();
  }, [selected]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Reports</h1>
        <p className="text-sm text-muted-foreground">
          Pick a job to see all screening reports for it.
        </p>
      </div>

      <Card>
        <CardContent className="p-4">
          <div className="flex flex-wrap gap-2">
            {jobs.length === 0 ? (
              <p className="text-sm text-muted-foreground">No jobs yet.</p>
            ) : (
              jobs.map((j) => (
                <Button
                  key={j.id}
                  variant={selected === j.id ? "default" : "outline"}
                  size="sm"
                  onClick={() => setSelected(j.id)}
                >
                  {j.title}
                </Button>
              ))
            )}
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        {rows.map((r) => (
          <Card key={r.screening_id}>
            <CardContent className="p-4 space-y-2">
              <div className="flex items-center justify-between">
                <div className="font-medium">
                  #{r.rank} · {r.candidate_name || `Resume #${r.resume_id}`}
                </div>
                <div className="text-sm">{r.ats_score.toFixed(1)}</div>
              </div>
              <div className="text-xs text-muted-foreground">{r.email || "—"}</div>
              <Link href={`/reports/${r.screening_id}`}>
                <Button size="sm" variant="outline" className="w-full">
                  Open report
                </Button>
              </Link>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
