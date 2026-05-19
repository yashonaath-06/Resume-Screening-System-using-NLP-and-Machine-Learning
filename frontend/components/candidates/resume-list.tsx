"use client";
import * as React from "react";
import { Trash2, FileText, Mail, Phone } from "lucide-react";
import { toast } from "sonner";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";
import type { Resume } from "@/lib/types";

interface Props {
  resumes: Resume[];
  onChange: () => void;
}

export function ResumeList({ resumes, onChange }: Props) {
  const handleDelete = async (id: number) => {
    if (!confirm("Delete this resume?")) return;
    try {
      await api.deleteResume(id);
      toast.success("Resume deleted");
      onChange();
    } catch (e) {
      toast.error((e as Error).message);
    }
  };

  if (!resumes.length) {
    return (
      <Card>
        <CardContent className="py-10 text-center text-muted-foreground">
          No resumes yet. Upload some from the Upload page.
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      {resumes.map((r) => (
        <Card key={r.id}>
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <FileText className="h-4 w-4 text-primary" />
              {r.candidate_name || r.file_name}
            </CardTitle>
            <p className="text-xs text-muted-foreground">
              {formatDate(r.created_at)} · {r.file_type.toUpperCase()}
            </p>
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            <div className="space-y-1">
              {r.email ? (
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Mail className="h-3.5 w-3.5" /> {r.email}
                </div>
              ) : null}
              {r.phone ? (
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Phone className="h-3.5 w-3.5" /> {r.phone}
                </div>
              ) : null}
            </div>
            <div className="flex gap-2 text-xs text-muted-foreground">
              <span>{r.experience_years} yrs experience</span>
              <span>·</span>
              <span>{r.skills.length} skills</span>
              <span>·</span>
              <span>{r.education.length} edu</span>
            </div>
            <div className="flex flex-wrap gap-1">
              {r.skills.slice(0, 8).map((s) => (
                <Badge key={s} variant="outline">{s}</Badge>
              ))}
              {r.skills.length > 8 ? (
                <Badge variant="outline">+{r.skills.length - 8} more</Badge>
              ) : null}
            </div>
            <div className="flex justify-end pt-2">
              <Button
                size="sm"
                variant="ghost"
                className="text-rose-500 hover:text-rose-600"
                onClick={() => handleDelete(r.id)}
              >
                <Trash2 className="h-3.5 w-3.5" />
                Delete
              </Button>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
