"""Publish the portfolio: snapshot content -> build static site -> deploy to Vercel -> push to Git.

Used by the "Publier" button of the local admin, or from a terminal:
    python publish.py [--no-deploy] [--no-git]
"""
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"


def step(title):
    print(f"\n=== {title} ===", flush=True)


def tool_env():
    """Environment with the usual Node/npm folders added, for icon launches with a short PATH."""
    env = os.environ.copy()
    extra = [Path(os.environ.get("APPDATA", "")) / "npm", Path(os.environ.get("ProgramFiles", "")) / "nodejs"]
    env["PATH"] = os.pathsep.join([str(p) for p in extra if p.exists()] + [env.get("PATH", "")])
    return env


def run(cmd, cwd=ROOT):
    result = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", env=tool_env())
    out = (result.stdout or "") + (result.stderr or "")
    print(out.strip(), flush=True)
    return result.returncode == 0


def find_vercel():
    """Locate the Vercel CLI even when PATH is minimal (e.g. launched from a desktop icon)."""
    for name in ("vercel.cmd", "vercel"):
        found = shutil.which(name)
        if found:
            return found
    candidates = [Path(os.environ.get("APPDATA", "")) / "npm" / "vercel.cmd",
                  Path(os.environ.get("ProgramFiles", "")) / "nodejs" / "vercel.cmd"]
    for path in candidates:
        if path.exists():
            return str(path)
    return None


def main(argv):
    deploy = "--no-deploy" not in argv
    use_git = "--no-git" not in argv
    ok = True

    step("1/4 Sauvegarde du contenu")
    from app import create_app
    from app.content_io import export_content
    app = create_app()
    with app.app_context():
        print(f"Contenu sauvegardé : {export_content().relative_to(ROOT)}")

    step("2/4 Génération du site")
    import export_static
    export_static.main()

    if deploy:
        step("3/4 Mise en ligne sur Vercel (bikoue.jsph.site)")
        (DIST / ".vercel").mkdir(exist_ok=True)
        shutil.copy(ROOT / "deploy" / "vercel-project.json", DIST / ".vercel" / "project.json")
        vercel = find_vercel()
        if not vercel:
            print("ÉCHEC : la commande 'vercel' est introuvable. Installez-la avec : npm i -g vercel")
            ok = False
        elif run(f'"{vercel}" deploy --prod --yes', cwd=DIST):
            print("Site en ligne.")
        else:
            print("ÉCHEC du déploiement Vercel (êtes-vous connecté ? commande : vercel login).")
            ok = False

    if use_git:
        step("4/4 Sauvegarde sur Git")
        run("git add -A")
        stamp = datetime.now().strftime("%d/%m/%Y %H:%M")
        if run(f'git commit -m "Mise à jour du site ({stamp})" -m "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"'):
            if not run("git push"):
                print("Le push Git a échoué (réseau ?). Le commit est enregistré en local.")
                ok = False
        else:
            print("Rien de nouveau à sauvegarder sur Git.")

    print("\nTERMINÉ" if ok else "\nTERMINÉ AVEC DES ERREURS (voir ci-dessus)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
