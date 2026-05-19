"use client";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { cn, scoreColor } from "@/lib/utils";
import type { RankedCandidate } from "@/lib/types";
import { FileText, Trophy } from "lucide-react";

interface Props {
  rows: RankedCandidate[];
}

export function CandidateTable({ rows }: Props) {
  if (!rows.length) {
    return (
      <Card>
        <CardContent className="py-10 text-center text-muted-foreground">
          No screenings yet. Run a screening from the Jobs page.
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Trophy className="h-4 w-4 text-primary" />
          Ranked candidates
        </CardTitle>
      </CardHeader>
      <CardContent className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-muted-foreground border-b">
              <th className="py-2 pr-4">#</th>
              <th className="py-2 pr-4">Candidate</th>
              <th className="py-2 pr-4">ATS</th>
              <th className="py-2 pr-4">Similarity</th>
              <th className="py-2 pr-4">Matched / Missing</th>
              <th className="py-2 pr-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((c) => (
              <tr key={c.screening_id} className="border-b last:border-0">
                <td className="py-3 pr-4 text-muted-foreground">{c.rank}</td>
                <td className="py-3 pr-4">
                  <div className="font-medium">{c.candidate_name || `Resume #${c.resume_id}`}</div>
                  <div className="text-xs text-muted-foreground">{c.email || "—"}</div>
                </td>
                <td className="py-3 pr-4 w-44">
                  <div className={cn("font-semibold", scoreColor(c.ats_score))}>
                    {c.ats_score.toFixed(1)}
                  </div>
                  <Progress value={c.ats_score} className="mt-1" />
                </td>
                <td className="py-3 pr-4 w-32 text-muted-foreground">
                  {(c.similarity * 100).toFixed(1)}%
                </td>
                <td className="py-3 pr-4 max-w-md">
                  <div className="flex flex-wrap gap-1">
                    {c.matched_skills.slice(0, 5).map((s) => (
                      <Badge key={s} variant="success">{s}</Badge>
                    ))}
                    {c.missing_skills.slice(0, 4).map((s) => (
                      <Badge key={s} variant="danger">{s}</Badge>
                    ))}
                  </div>
                </td>
                <td className="py-3 pr-4 text-right">
                  <Link href={`/reports/${c.screening_id}`}>
                    <Button size="sm" variant="outline">
                      <FileText className="h-3.5 w-3.5" />
                      Report
                    </Button>
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </CardContent>
    </Card>
  );
}
