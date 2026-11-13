import Std

namespace FunnelScript.Formal

/-!
A domain-neutral, discrete-time abstraction of EventMachine v0.
Time is a natural number rather than the finite non-negative float of the
Python implementation. The abstraction does not establish float/PRNG parity.
-/

structure Event where
  time : Nat
  priority : Int
  ordinal : Nat
  name : String
  deriving Repr, Inhabited, DecidableEq

structure EventDraft where
  time : Nat
  priority : Int
  name : String
  deriving Repr, Inhabited, DecidableEq

structure Transition (σ : Type) where
  state : σ
  seed : Nat
  emitted : List EventDraft

abbrev Reducer (σ : Type) := σ → Event → Nat → Transition σ

structure Machine (σ : Type) where
  state : σ
  seed : Nat
  clock : Nat
  nextOrdinal : Nat
  pending : List Event

/-- Lexicographic ordering: timestamp, priority, insertion ordinal. -/
def eventLE (a b : Event) : Bool :=
  if a.time < b.time then true
  else if b.time < a.time then false
  else if a.priority < b.priority then true
  else if b.priority < a.priority then false
  else decide (a.ordinal ≤ b.ordinal)

/-- A list implementation of the Python heap's selection policy. -/
def sortedCalendar (events : List Event) : List Event :=
  events.mergeSort eventLE

/-- Allocate stable, increasing ordinals to locally emitted events. -/
def stamp : Nat → List EventDraft → List Event × Nat
  | next, [] => ([], next)
  | next, e :: es =>
      let (tail, last) := stamp (next + 1) es
      ({ time := e.time, priority := e.priority,
         ordinal := next, name := e.name } :: tail, last)

/-- Enforce causal time and forbid priority retrogression at equal time. -/
def legalEmissions (parent : Event) (events : List EventDraft) : Bool :=
  events.all fun e => decide
    (parent.time ≤ e.time ∧
     (e.time = parent.time → parent.priority ≤ e.priority))

/-- Evidence carried by a successful, machine-checked kernel step. -/
structure Advance {σ : Type} (previous : Machine σ) where
  event : Event
  next : Machine σ
  legalTime : previous.clock ≤ event.time
  nextClock : next.clock = event.time

/-- A finite-step executable kernel with explicit rejection of illegal emissions. -/
def advance {σ : Type} (reduce : Reducer σ)
    (machine : Machine σ) : Option (Advance machine) :=
  match sortedCalendar machine.pending with
  | [] => none
  | event :: remaining =>
      if legal : machine.clock ≤ event.time then
        let transition := reduce machine.state event machine.seed
        if legalEmissions event transition.emitted then
          let (generated, nextOrdinal) :=
            stamp machine.nextOrdinal transition.emitted
          let next : Machine σ := {
            state := transition.state
            seed := transition.seed
            clock := event.time
            nextOrdinal := nextOrdinal
            pending := remaining ++ generated
          }
          some {
            event := event
            next := next
            legalTime := legal
            nextClock := rfl
          }
        else none
      else none

/-- Processing fuel is the event limit; pending events remain when fuel expires. -/
def run {σ : Type} (reduce : Reducer σ) :
    Nat → Machine σ → Machine σ × List Event
  | 0, machine => (machine, [])
  | fuel + 1, machine =>
      match advance reduce machine with
      | none => (machine, [])
      | some step =>
          let (final, trace) := run reduce fuel step.next
          (final, step.event :: trace)

/-- Each event is at or later than the preceding processed timestamp. -/
def ChronologicalFrom (clock : Nat) : List Event → Prop
  | [] => True
  | event :: rest =>
      clock ≤ event.time ∧ ChronologicalFrom event.time rest

end FunnelScript.Formal
