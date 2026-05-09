import { RoutineForm } from "@/components/routine-form";

export const metadata = { title: "New Routine — Control Panel" };

export default function RoutineNewPage() {
  return (
    <div className="max-w-3xl">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold tracking-tight">New Routine</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Schedule a recipe to run automatically via APScheduler.
        </p>
      </div>
      <RoutineForm />
    </div>
  );
}
