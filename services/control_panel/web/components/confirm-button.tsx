"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

// A trigger Button that opens a small confirm dialog before firing
// `onConfirm`. Matches the codebase's pattern: `open` is managed locally
// (no DialogTrigger) so it interoperates cleanly with surrounding flows.
//
// Used for destructive actions like Uninstall where an accidental click
// would tear something down without a second beat.
type ButtonVariant =
  | "default"
  | "destructive"
  | "outline"
  | "secondary"
  | "ghost"
  | "link";

type Props = {
  children: React.ReactNode; // trigger label
  title: string;
  description?: string;
  confirmLabel?: string;
  // Destructive defaults — Uninstall-shaped. Override for benign confirms.
  confirmVariant?: ButtonVariant;
  triggerVariant?: ButtonVariant;
  size?: "default" | "sm";
  disabled?: boolean;
  onConfirm: () => void;
};

export function ConfirmButton({
  children,
  title,
  description,
  confirmLabel = "Confirm",
  confirmVariant = "destructive",
  triggerVariant = "outline",
  size = "sm",
  disabled = false,
  onConfirm,
}: Props) {
  const [open, setOpen] = useState(false);

  return (
    <>
      <Button
        type="button"
        size={size}
        variant={triggerVariant}
        disabled={disabled}
        onClick={() => setOpen(true)}
      >
        {children}
      </Button>
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>{title}</DialogTitle>
            {description && <DialogDescription>{description}</DialogDescription>}
          </DialogHeader>
          <DialogFooter className="gap-2 sm:gap-2">
            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={() => setOpen(false)}
            >
              Cancel
            </Button>
            <Button
              type="button"
              variant={confirmVariant}
              size="sm"
              onClick={() => {
                setOpen(false);
                onConfirm();
              }}
            >
              {confirmLabel}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
