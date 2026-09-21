# app/styles/tokens.py

# ---------- Brand / Theme Colors ----------

PRIMARY = "#06B6D4"      # cyan
SECONDARY = "#1E293B"    # slate
ACCENT = "#8B5CF6"       # violet

POSITIVE = "#10B981"
NEGATIVE = "#EF4444"
WARNING = "#F59E0B"
INFO = "#38BDF8"


# ---------- Reusable Layout Classes ----------

PAGE = (
    "w-full min-h-screen "
    "bg-slate-950 text-slate-100"
)

CONTENT = (
    "w-full max-w-screen-2xl "
    "mx-auto p-6"
)

SURFACE = (
    "bg-slate-900 "
    "border border-slate-800 "
    "rounded-2xl"
)

CARD = (
    SURFACE
    + " p-5"
)

CARD_INTERACTIVE = (
    CARD
    + " hover:border-slate-700 "
      "transition-colors cursor-pointer"
)


# ---------- Typography ----------

EYEBROW = (
    "text-xs font-semibold uppercase "
    "tracking-widest text-cyan-400"
)

PAGE_TITLE = (
    "text-3xl font-semibold tracking-tight"
)

SECTION_TITLE = (
    "text-xl font-semibold tracking-tight"
)

BODY = (
    "text-sm text-slate-300"
)

MUTED = (
    "text-sm text-slate-400"
)

METRIC = (
    "text-3xl font-semibold tracking-tight"
)