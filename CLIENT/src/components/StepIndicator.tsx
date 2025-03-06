import { cn } from "@/lib/utils";
import { BadgeCheck, Loader2 } from "lucide-react";
import { Step } from "../types";

interface StepIndicatorProps {
  steps: Step[];
}

const StepIndicator: React.FC<StepIndicatorProps> = ({ steps }) => {
  console.log("StepIndicator received steps:", steps);

  return (
    <div className="space-y-5 my-3">
      {steps.map((s, index) => (
        <div
          key={index}
          className="flex items-center gap-4 transition-all duration-300"
        >
          <div className="flex-shrink-0 relative">
            {s.completed ? (
              <BadgeCheck className="w-6 h-6 text-green-600" />
            ) : (
              <Loader2 className="w-6 h-6 animate-spin text-teal-600" />
            )}
            <div
              className={cn(
                "absolute -inset-1 rounded-full opacity-20",
                s.completed ? "bg-green-200" : "bg-teal-200"
              )}
            />
          </div>
          <span
            className={cn(
              "text-sm font-medium transition-colors duration-200",
              s.completed ? "text-gray-600" : "text-teal-600"
            )}
          >
            {s.text}
          </span>
          {index < steps.length - 1 && (
            <div className="flex-1 h-px bg-gray-300 ml-3 border-dashed border-gray-400" />
          )}
        </div>
      ))}
    </div>
  );
};

export default StepIndicator;
