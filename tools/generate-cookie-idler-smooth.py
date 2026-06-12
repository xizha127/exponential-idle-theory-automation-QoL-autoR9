from pathlib import Path
from urllib.request import urlopen

SOURCE_URL = "https://raw.githubusercontent.com/KS-Sainen/Custom-Theory-Cookie-Idler/main/CookieIdler%20-%20Redux.js"
OUT = Path("CookieIdler-Redux.smooth-counter.js")

SMOOTH_HELPERS = r'''

// Smooth online cookie flow.
// The original game logic pays each building in chunks every collectionTime ticks.
// This helper keeps the same per-collection amount, but distributes it over each tick.
// That makes the visible cookie counter flow continuously without rewriting the economy.
var generateSmoothCookie = (id, dt, mult) => {
    if(id < 0 || id >= buildingData.length){return BF(0);}
    if(building[id].level <= 0 && investHelp[id].level <= 0){return BF(0);}
    let ct = buildingData[id].collectionTime;
    if(Number.isNaN(ct) || ct <= 0){return BF(0);}
    return generateCookie(id, ct, mult) * (dt / ct);
}

var generateSmoothCookieGain = (dt, mult) => {
    let ret = BF(0);
    for(let i=0;i<19;i++){
        ret += generateSmoothCookie(i, dt, mult);
    }
    return ret;
}
'''

OLD_ONLINE_BLOCK = r'''        //cookie
        if(thyme.level % 5 == 0){
            if(CHAOS_STAGE.level > 2){
                updateChaosBuildingName();
            }
            if(dt >= buildingData[dominate].collection){
                cookieGain += generateCookie(dominate,dt,terraBoost);
            }else{
                for(let i=0;i<=9;i++){
                    let id = i*2;
                    if(dt >= buildingData[id].collectionTime){
                        cookieGain += generateCookie(id,dt,terraBoost);
                        if(id < 18)cookieGain += generateCookie(id+1,dt,terraBoost);
                    }else if(thyme.level % buildingData[id].collectionTime == 0){
                        //log(`${i} due!`);
                        cookieGain += generateCookie(id,buildingData[id].collectionTime,terraBoost);
                        if(id < 18)cookieGain += generateCookie(id+1,buildingData[id+1].collectionTime,terraBoost);
                    }
                }
            }
            if(thyme.level % 2 == 0){//5 * 2 = 10
'''

NEW_ONLINE_BLOCK = r'''        //cookie
        // Smooth mode: pay buildings continuously instead of waiting for collectionTime boundaries.
        // This preserves each building's full-collection value by prorating it over dt.
        cookieGain += generateSmoothCookieGain(dt,terraBoost);
        if(thyme.level % 5 == 0){
            if(CHAOS_STAGE.level > 2){
                updateChaosBuildingName();
            }
            if(thyme.level % 2 == 0){//5 * 2 = 10
'''

def main() -> None:
    src = urlopen(SOURCE_URL, timeout=30).read().decode("utf-8")

    anchor = "    //log(`get ${ret}`);\n    //log(`generating for ${id}, base = ${ret}, pow = ${pow}`);\n    return ret;\n}\nvar generateLump = (ticks) => {"
    if anchor not in src:
        raise RuntimeError("Could not locate generateCookie insertion anchor.")
    src = src.replace(anchor, anchor.replace("\nvar generateLump", SMOOTH_HELPERS + "\nvar generateLump"), 1)

    if OLD_ONLINE_BLOCK not in src:
        raise RuntimeError("Could not locate original online cookie gain block.")
    src = src.replace(OLD_ONLINE_BLOCK, NEW_ONLINE_BLOCK, 1)

    OUT.write_text(src, encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
