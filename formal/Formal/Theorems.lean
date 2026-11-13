import Formal.Kernel

namespace FunnelScript.Formal

/-- Every successfully executed event respects the preceding clock. -/
theorem timestamp_monotonicity {σ : Type} (reduce : Reducer σ) :
    (fuel : Nat) → (initial : Machine σ) →
      ChronologicalFrom initial.clock (run reduce fuel initial).2 := by
  intro fuel
  induction fuel with
  | zero =>
      intro initial
      simp [run, ChronologicalFrom]
  | succ fuel ih =>
      intro initial
      cases h : advance reduce initial with
      | none =>
          simp [run, h, ChronologicalFrom]
      | some step =>
          have tail :
              ChronologicalFrom step.event.time
                (run reduce fuel step.next).2 := by
            simpa [step.nextClock] using ih step.next
          simpa [run, h, ChronologicalFrom] using
            (And.intro step.legalTime tail)

/-- A fixed pure reducer and identical complete input give identical replay. -/
theorem deterministic_replay {σ : Type} (reduce : Reducer σ)
    (fuel : Nat) (first second : Machine σ)
    (sameInput : first = second) :
    run reduce fuel first = run reduce fuel second := by
  cases sameInput
  rfl

/-- The small-step transition is functional: two results cannot diverge. -/
theorem unique_advance {σ : Type} (reduce : Reducer σ)
    (initial : Machine σ) (a b : Advance initial)
    (ha : advance reduce initial = some a)
    (hb : advance reduce initial = some b) : a = b := by
  rw [ha] at hb
  cases hb
  rfl

end FunnelScript.Formal

#print axioms FunnelScript.Formal.timestamp_monotonicity
#print axioms FunnelScript.Formal.deterministic_replay
#print axioms FunnelScript.Formal.unique_advance
