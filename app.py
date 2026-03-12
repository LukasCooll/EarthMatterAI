import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import threading
import os
import sys

# ── Colour palette ──────────────────────────────────────────────────────────
BG         = "#F4F7F2"   # soft sage white
SURFACE    = "#FFFFFF"
CARD       = "#EDF2EB"
BORDER     = "#D4E0CF"
GREEN_DARK = "#2D6A4F"   # deep forest
GREEN_MID  = "#52B788"   # leaf
GREEN_LT   = "#95D5B2"   # mint
AMBER      = "#E9C46A"
RED        = "#E07A5F"
TEXT       = "#1B2B1E"
MUTED      = "#7A9E87"
WHITE      = "#FFFFFF"

FONT_H1    = ("Georgia", 22, "bold")
FONT_H2    = ("Georgia", 13, "bold")
FONT_BODY  = ("Helvetica Neue", 11)
FONT_MONO  = ("Courier", 10)
FONT_SMALL = ("Helvetica Neue", 9)

# ── App ──────────────────────────────────────────────────────────────────────
class UrbanEyeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UrbanEye — Environment Analysis")
        self.geometry("1060x740")
        self.minsize(860, 620)
        self.configure(bg=BG)
        self.resizable(True, True)

        self.img_path   = tk.StringVar(value="No image selected")
        self.model_path = tk.StringVar(value="yolov8x-oiv7.pt")
        self.conf_var   = tk.DoubleVar(value=0.25)
        self.iou_var    = tk.DoubleVar(value=0.45)
        self.running    = False

        self._build_header()
        self._build_body()
        self._build_status_bar()

    # ── Header ──────────────────────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self, bg=GREEN_DARK, height=64)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        leaf = tk.Label(hdr, text="🌿", font=("", 22), bg=GREEN_DARK)
        leaf.pack(side="left", padx=(20, 6), pady=12)

        title = tk.Label(hdr, text="UrbanEye", font=FONT_H1,
                         fg=WHITE, bg=GREEN_DARK)
        title.pack(side="left")

        sub = tk.Label(hdr, text="  Urban Environment Analyser",
                       font=("Helvetica Neue", 11), fg=GREEN_LT, bg=GREEN_DARK)
        sub.pack(side="left", pady=4)

        self.run_btn = tk.Button(
            hdr, text="▶  Run Analysis",
            font=("Helvetica Neue", 11, "bold"),
            bg=GREEN_MID, fg=WHITE, activebackground=GREEN_LT,
            activeforeground=GREEN_DARK, relief="flat",
            padx=18, pady=6, cursor="hand2",
            command=self._start_analysis
        )
        self.run_btn.pack(side="right", padx=20, pady=12)

    # ── Body ─────────────────────────────────────────────────────────────────
    def _build_body(self):
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=20, pady=16)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        # Left panel
        left = tk.Frame(body, bg=BG, width=290)
        left.grid(row=0, column=0, sticky="ns", padx=(0, 14))
        left.pack_propagate(False)
        self._build_left(left)

        # Right panel
        right = tk.Frame(body, bg=BG)
        right.grid(row=0, column=1, sticky="nsew")
        self._build_right(right)

    # ── Left ─────────────────────────────────────────────────────────────────
    def _build_left(self, parent):
        # Image card
        img_card = self._card(parent, "📷  Image")
        img_card.pack(fill="x", pady=(0, 10))

        self.img_thumb = tk.Label(img_card, bg=CARD, text="No image\nselected",
                                  font=FONT_SMALL, fg=MUTED,
                                  width=28, height=8, relief="flat")
        self.img_thumb.pack(fill="x", padx=12, pady=(4, 8))

        tk.Button(img_card, text="Choose Image…",
                  font=FONT_BODY, bg=GREEN_DARK, fg=WHITE,
                  activebackground=GREEN_MID, relief="flat",
                  padx=10, pady=5, cursor="hand2",
                  command=self._choose_image
                  ).pack(fill="x", padx=12, pady=(0, 12))

        path_lbl = tk.Label(img_card, textvariable=self.img_path,
                            font=FONT_SMALL, fg=MUTED, bg=SURFACE,
                            wraplength=230, anchor="w")
        path_lbl.pack(fill="x", padx=12, pady=(0, 10))

        # Model card
        model_card = self._card(parent, "⚙  Model & Thresholds")
        model_card.pack(fill="x", pady=(0, 10))

        self._labeled_entry(model_card, "Model path", self.model_path)

        self._slider_row(model_card, "Conf threshold", self.conf_var, 0.0, 1.0)
        self._slider_row(model_card, "IoU  threshold", self.iou_var,  0.0, 1.0)

        tk.Frame(model_card, bg=SURFACE, height=12).pack()

        # Index card (live values updated after run)
        idx_card = self._card(parent, "📊  Indices")
        idx_card.pack(fill="x", pady=(0, 10))

        self.idx_frames = {}
        for label, color in [("Green Coverage",  GREEN_MID),
                              ("Traffic Density", AMBER),
                              ("Human Activity",  RED)]:
            row = tk.Frame(idx_card, bg=SURFACE)
            row.pack(fill="x", padx=12, pady=4)
            tk.Label(row, text=label, font=FONT_SMALL, fg=TEXT,
                     bg=SURFACE, anchor="w").pack(side="left")
            val = tk.Label(row, text="—", font=("Helvetica Neue", 11, "bold"),
                           fg=color, bg=SURFACE)
            val.pack(side="right")
            self.idx_frames[label] = val

        tk.Frame(idx_card, bg=SURFACE, height=10).pack()

    # ── Right ────────────────────────────────────────────────────────────────
    def _build_right(self, parent):
        parent.rowconfigure(1, weight=1)
        parent.columnconfigure(0, weight=1)

        # Detection counts bar
        count_card = self._card(parent, "🔍  Detected Objects")
        count_card.grid(row=0, column=0, sticky="ew", pady=(0, 12))

        self.count_inner = tk.Frame(count_card, bg=SURFACE)
        self.count_inner.pack(fill="x", padx=12, pady=(4, 12))
        self._render_count_chips({})

        # Console / log
        log_card = self._card(parent, "📋  Analysis Log")
        log_card.grid(row=1, column=0, sticky="nsew")
        log_card.rowconfigure(1, weight=1)
        log_card.columnconfigure(0, weight=1)

        self.console = scrolledtext.ScrolledText(
            log_card, bg="#1B2B1E", fg="#95D5B2",
            font=FONT_MONO, relief="flat",
            wrap="word", state="disabled",
            insertbackground=GREEN_LT,
            selectbackground=GREEN_MID
        )
        self.console.pack(fill="both", expand=True, padx=12, pady=(4, 12))

        # Tag styles
        self.console.tag_config("head",  foreground=GREEN_LT,  font=("Courier", 10, "bold"))
        self.console.tag_config("ok",    foreground=GREEN_MID)
        self.console.tag_config("warn",  foreground=AMBER)
        self.console.tag_config("err",   foreground=RED)
        self.console.tag_config("muted", foreground=MUTED)

        btn_row = tk.Frame(log_card, bg=SURFACE)
        btn_row.pack(fill="x", padx=12, pady=(0, 10))
        tk.Button(btn_row, text="Clear", font=FONT_SMALL,
                  bg=CARD, fg=MUTED, relief="flat", padx=10, pady=3,
                  cursor="hand2", command=self._clear_log
                  ).pack(side="right")

        self._log("UrbanEye ready. Choose an image and press Run Analysis.", "muted")

    # ── Status bar ───────────────────────────────────────────────────────────
    def _build_status_bar(self):
        bar = tk.Frame(self, bg=BORDER, height=28)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)

        self.status_var = tk.StringVar(value="Idle")
        tk.Label(bar, textvariable=self.status_var,
                 font=FONT_SMALL, fg=MUTED, bg=BORDER, anchor="w"
                 ).pack(side="left", padx=14)

        self.progress = ttk.Progressbar(bar, mode="indeterminate", length=140)
        self.progress.pack(side="right", padx=14, pady=5)

    # ── Helpers ──────────────────────────────────────────────────────────────
    def _card(self, parent, title):
        outer = tk.Frame(parent, bg=SURFACE, bd=0,
                         highlightthickness=1, highlightbackground=BORDER)
        outer.pack_propagate(True)
        tk.Label(outer, text=title, font=FONT_H2,
                 fg=GREEN_DARK, bg=SURFACE, anchor="w",
                 padx=12, pady=8).pack(fill="x")
        tk.Frame(outer, bg=BORDER, height=1).pack(fill="x")
        return outer

    def _labeled_entry(self, parent, label, var):
        tk.Label(parent, text=label, font=FONT_SMALL,
                 fg=MUTED, bg=SURFACE, anchor="w"
                 ).pack(fill="x", padx=12, pady=(8, 2))
        e = tk.Entry(parent, textvariable=var, font=FONT_MONO,
                     bg=CARD, fg=TEXT, relief="flat",
                     highlightthickness=1, highlightbackground=BORDER)
        e.pack(fill="x", padx=12, pady=(0, 4))

    def _slider_row(self, parent, label, var, lo, hi):
        row = tk.Frame(parent, bg=SURFACE)
        row.pack(fill="x", padx=12, pady=3)
        tk.Label(row, text=label, font=FONT_SMALL,
                 fg=MUTED, bg=SURFACE, width=16, anchor="w").pack(side="left")
        val_lbl = tk.Label(row, text=f"{var.get():.2f}",
                           font=FONT_MONO, fg=GREEN_DARK, bg=SURFACE, width=5)
        val_lbl.pack(side="right")
        s = tk.Scale(row, variable=var, from_=lo, to=hi, resolution=0.01,
                     orient="horizontal", bg=SURFACE, fg=TEXT,
                     troughcolor=CARD, activebackground=GREEN_MID,
                     highlightthickness=0, showvalue=False,
                     command=lambda v, l=val_lbl, dv=var: l.config(text=f"{float(v):.2f}"))
        s.pack(side="left", fill="x", expand=True, padx=6)

    def _render_count_chips(self, counts):
        for w in self.count_inner.winfo_children():
            w.destroy()
        if not counts:
            tk.Label(self.count_inner, text="No detections yet.",
                     font=FONT_SMALL, fg=MUTED, bg=SURFACE).pack(anchor="w")
            return
        icons = {'Tree':'🌳','Plant':'🌿','Person':'🚶','Car':'🚗',
                 'Truck':'🚚','Bus':'🚌','Motorcycle':'🏍',
                 'Vehicle':'🚙','Flowerpot':'🪴','Houseplant':'🪴'}
        row = tk.Frame(self.count_inner, bg=SURFACE)
        row.pack(fill="x")
        col = 0
        for cls, cnt in sorted(counts.items()):
            if cnt == 0:
                continue
            chip = tk.Frame(row, bg=CARD, padx=8, pady=4,
                            highlightthickness=1, highlightbackground=BORDER)
            chip.grid(row=0, column=col, padx=4, pady=4)
            tk.Label(chip, text=icons.get(cls, "●"),
                     font=("", 14), bg=CARD).pack()
            tk.Label(chip, text=f"{cls}\n{cnt}",
                     font=FONT_SMALL, fg=TEXT, bg=CARD,
                     justify="center").pack()
            col += 1

    def _log(self, msg, tag="ok"):
        self.console.config(state="normal")
        self.console.insert("end", msg + "\n", tag)
        self.console.see("end")
        self.console.config(state="disabled")

    def _clear_log(self):
        self.console.config(state="normal")
        self.console.delete("1.0", "end")
        self.console.config(state="disabled")

    def _choose_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.webp"), ("All", "*.*")])
        if not path:
            return
        self._set_image(path)

    def _set_image(self, path):
        self._full_img_path = path
        self.img_path.set(os.path.basename(path))

        try:
            from PIL import Image, ImageTk
            img = Image.open(path)
            img.thumbnail((240, 140))
            photo = ImageTk.PhotoImage(img)
            self.img_thumb.config(image=photo, text="")
            self.img_thumb._photo = photo   # keep reference
        except ImportError:
            self.img_thumb.config(text="(PIL not installed\nfor preview)")

    # ── Analysis ─────────────────────────────────────────────────────────────
    def _start_analysis(self):
        if self.running:
            return
        if not hasattr(self, "_full_img_path"):
            # Mirror ObjRecognition.py line 10: IMG_PATH = GettingFile.Save_Root()
            try:
                import GettingFile
                path = GettingFile.Save_Root()
                if path:
                    self._set_image(path)
                    self._log(f"ℹ  Using GettingFile.Save_Root(): {path}", "muted")
                else:
                    self._log("⚠  Please choose an image first.", "warn")
                    return
            except Exception as e:
                self._log(f"⚠  Please choose an image first. ({e})", "warn")
                return

        self.running = True
        self.run_btn.config(state="disabled", bg=MUTED)
        self.status_var.set("Running analysis…")
        self.progress.start(12)

        t = threading.Thread(target=self._run_pipeline, daemon=True)
        t.start()

    def _run_pipeline(self):
        try:
            self._log("\n══ Starting Analysis ══", "head")
            self._log(f"Image : {self._full_img_path}", "muted")
            self._log(f"Model : {self.model_path.get()}", "muted")
            self._log(f"Conf  : {self.conf_var.get():.2f}  IoU: {self.iou_var.get():.2f}", "muted")

            # ── YOLO ──────────────────────────────────────────────────────
            self._log("\n▸ Loading YOLO model…", "head")
            from ultralytics import YOLO
            import torch

            TARGET_CLASSES = {
                'Tree', 'Plant', 'Person', 'Car', 'Truck',
                'Bus', 'Motorcycle', 'Vehicle', 'Flowerpot', 'Houseplant'
            }

            model = YOLO(self.model_path.get())
            self._log("  Model loaded ✓", "ok")

            self._log("▸ Running standard YOLO inference…", "head")
            results = model(
                self._full_img_path,
                conf=self.conf_var.get(),
                iou=self.iou_var.get(),
                imgsz=1280,
                augment=True,
                agnostic_nms=True,
                verbose=False,
            )

            counts = {n: 0 for n in TARGET_CLASSES}
            for box in results[0].boxes:
                name = model.names[int(box.cls.item())]
                conf = float(box.conf.item())
                if name in TARGET_CLASSES:
                    counts[name] += 1
                    self._log(f"  Detected: {name:<15} conf={conf:.2f}")

            self._log("\n  YOLO counts:", "head")
            for cls, cnt in sorted(counts.items()):
                if cnt:
                    self._log(f"    {cls:<15}: {cnt}")

            # ── SAHI ──────────────────────────────────────────────────────
            self._log("\n▸ Running SAHI sliced inference…", "head")
            from sahi import AutoDetectionModel
            from sahi.predict import get_sliced_prediction

            sahi_model = AutoDetectionModel.from_pretrained(
                model_type='yolov8',
                model_path=self.model_path.get(),
                confidence_threshold=self.conf_var.get(),
                device='cuda:0' if torch.cuda.is_available() else 'cpu',
            )
            sahi_result = get_sliced_prediction(
                self._full_img_path, sahi_model,
                slice_height=640, slice_width=640,
                overlap_height_ratio=0.2, overlap_width_ratio=0.2,
            )

            sahi_counts = {n: 0 for n in TARGET_CLASSES}
            for obj in sahi_result.object_prediction_list:
                name = obj.category.name
                if name in TARGET_CLASSES:
                    sahi_counts[name] += 1

            self._log("\n  SAHI counts:", "head")
            for cls, cnt in sorted(sahi_counts.items()):
                if cnt:
                    self._log(f"    {cls:<15}: {cnt}")

            sahi_result.export_visuals(export_dir="sahi_output/")
            self._log("  SAHI visual → sahi_output/", "muted")

            # ── Merge ─────────────────────────────────────────────────────
            merged = {c: max(counts[c], sahi_counts[c]) for c in TARGET_CLASSES}

            # ── Location & Climate ────────────────────────────────────────
            self._log("\n▸ Fetching location & climate…", "head")
            try:
                import location, GettingClimate
                geo_info  = location.get_ip_geolocation()
                lon       = location.get_longitute()
                lat       = location.get_latitute()
                climate   = GettingClimate.get_climate_data(lon, lat)
                self._log(f"  {geo_info}")
                self._log(f"  lat={lat}  lon={lon}")
                self._log(f"  Climate: {climate}")
            except Exception as e:
                self._log(f"  Location/climate skipped: {e}", "warn")
                lat, lon, geo_info, climate = "—", "—", "—", "—"

            # ── Indices ───────────────────────────────────────────────────
            total = sum(merged.values()) or 1
            green_idx   = round((merged.get('Tree',0) + merged.get('Plant',0) +
                                 merged.get('Houseplant',0) + merged.get('Flowerpot',0)) / total, 2)
            traffic_idx = round((merged.get('Car',0) + merged.get('Truck',0) +
                                 merged.get('Bus',0)  + merged.get('Motorcycle',0) +
                                 merged.get('Vehicle',0)) / total, 2)
            human_idx   = round(merged.get('Person',0) / total, 2)

            self._log("\n══ Final Report ══", "head")
            self._log(f"  Green Coverage Index : {green_idx}")
            self._log(f"  Traffic Density Index: {traffic_idx}")
            self._log(f"  Human Activity Index : {human_idx}")

            # ── AI Response ───────────────────────────────────────────────
            try:
                import AiResponce
                self._log("\n▸ Getting AI response…", "head")
                ai_text = AiResponce.GetPromptAndResponse(
                    green_idx=green_idx,
                    traffic_idx=traffic_idx,
                    human_idx=human_idx,
                    climate=climate,
                )
                self._log(ai_text, "ok")
                self._log("  AI response complete ✓")
            except Exception as e:
                self._log(f"  AI response skipped: {e}", "warn")

            # ── Update UI ─────────────────────────────────────────────────
            self.after(0, self._update_results, merged, green_idx, traffic_idx, human_idx)

        except Exception as e:
            self._log(f"\n✖ Error: {e}", "err")
        finally:
            self.after(0, self._analysis_done)

    def _update_results(self, merged, green_idx, traffic_idx, human_idx):
        self._render_count_chips(merged)
        self.idx_frames["Green Coverage"].config( text=f"{green_idx:.0%}")
        self.idx_frames["Traffic Density"].config(text=f"{traffic_idx:.0%}")
        self.idx_frames["Human Activity"].config( text=f"{human_idx:.0%}")

    def _analysis_done(self):
        self.running = False
        self.run_btn.config(state="normal", bg=GREEN_MID)
        self.progress.stop()
        self.status_var.set("Analysis complete")
        self._log("\n✔ Done.", "ok")


if __name__ == "__main__":
    app = UrbanEyeApp()
    app.mainloop()