"use client";
import * as React from "react";
import { ResumeUploader } from "@/components/upload/resume-uploader";
import { ResumeList } from "@/components/candidates/resume-list";
import { api } from "@/lib/api";
import type { Resume } from "@/lib/types";
import { toast } from "sonner";

export default function UploadPage() {
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
        <h1 className="text-2xl font-bold tracking-tight">Upload resumes</h1>
        <p className="text-sm text-muted-foreground">
          Drop PDF / DOCX / TXT files. They're parsed, cleaned, and indexed automatically.
        </p>
      </div>

      <ResumeUploader onUploaded={refresh} />

      <div>
        <h2 className="text-lg font-semibold mb-3">Library</h2>
        <ResumeList resumes={resumes} onChange={refresh} />
      </div>
    </div>
  );
}
