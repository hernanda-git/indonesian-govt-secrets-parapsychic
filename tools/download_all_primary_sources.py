import os
import json
import time
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = r"C:\Workspace\indonesian-govt-secrets-parapsychic"
SOURCES_DIR = os.path.join(ROOT, "declassified_primary_sources")
PDF_DIR = os.path.join(SOURCES_DIR, "pdf")
TXT_DIR = os.path.join(SOURCES_DIR, "txt")
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(TXT_DIR, exist_ok=True)

TARGET_DOCUMENTS = [
    # 1. Project GRILL FLAME - Tehran US Embassy Hostage Remote Viewing Sessions
    {
        "cat": "GRILL_FLAME_TEHRAN_EMBASSY",
        "id": "cia-readingroom-document-cia-rdp96-00788r000800340001-7",
        "name": "GRILL_FLAME_Session_42_Tehran_Hostage_US_Embassy",
        "desc": "DIA Project GRILL FLAME Session CC42 targeting the US Embassy compound in Tehran, Iran"
    },
    {
        "cat": "GRILL_FLAME_TEHRAN_EMBASSY",
        "id": "cia-readingroom-document-cia-rdp96-00788r000800050001-9",
        "name": "GRILL_FLAME_Session_CC9_Tehran_Hostage_US_Embassy",
        "desc": "Project GRILL FLAME Session CC9 targeting hostage locations in Tehran Embassy"
    },
    {
        "cat": "GRILL_FLAME_TEHRAN_EMBASSY",
        "id": "cia-readingroom-document-cia-rdp96-00788r000800110001-2",
        "name": "GRILL_FLAME_Session_16_Tehran_Hostage_US_Embassy",
        "desc": "GRILL FLAME RV Session 16 on US Embassy hostages and security sentries"
    },
    {
        "cat": "GRILL_FLAME_TEHRAN_EMBASSY",
        "id": "cia-readingroom-document-cia-rdp96-00788r000800200001-2",
        "name": "GRILL_FLAME_Session_CC26_Tehran_Hostage_US_Embassy",
        "desc": "Project GRILL FLAME Session CC26 evaluating hostage room layouts"
    },
    {
        "cat": "GRILL_FLAME_TEHRAN_EMBASSY",
        "id": "cia-readingroom-document-cia-rdp96-00788r000800260001-6",
        "name": "GRILL_FLAME_Session_CC33_Tehran_Hostage_US_Embassy",
        "desc": "Summary Remote Viewing Session CC33 targeting Chancery building"
    },
    {
        "cat": "GRILL_FLAME_TEHRAN_EMBASSY",
        "id": "cia-readingroom-document-cia-rdp96-00788r000800270001-5",
        "name": "GRILL_FLAME_Session_CC34_Tehran_Hostage_US_Embassy",
        "desc": "Summary Remote Viewing Session CC34 targeting diplomatic personnel in Tehran"
    },
    {
        "cat": "GRILL_FLAME_TEHRAN_EMBASSY",
        "id": "cia-readingroom-document-cia-rdp96-00788r000800390001-2",
        "name": "GRILL_FLAME_Session_CC47_Tehran_Hostage_US_Embassy",
        "desc": "Summary Remote Viewing Session CC47 on hostage movement"
    },
    {
        "cat": "GRILL_FLAME_TEHRAN_EMBASSY",
        "id": "cia-readingroom-document-cia-rdp96-00788r000800450001-5",
        "name": "GRILL_FLAME_Session_CC54_Tehran_Hostage_US_Embassy",
        "desc": "Summary Remote Viewing Session CC54 on embassy compound security"
    },
    {
        "cat": "GRILL_FLAME_TEHRAN_EMBASSY",
        "id": "cia-readingroom-document-cia-rdp96-00788r000800500001-9",
        "name": "GRILL_FLAME_Session_CC59_Tehran_Hostage_US_Embassy",
        "desc": "Summary Remote Viewing Session CC59 targeting ambassadorial residence"
    },
    {
        "cat": "GRILL_FLAME_TEHRAN_EMBASSY",
        "id": "cia-readingroom-document-cia-rdp96-00788r000800880001-8",
        "name": "GRILL_FLAME_Session_CCC63_Tehran_Hostage_US_Embassy",
        "desc": "Summary Remote Viewing Session CCC63 correlation analysis"
    },
    {
        "cat": "GRILL_FLAME_TEHRAN_EMBASSY",
        "id": "cia-readingroom-document-cia-rdp96-00791r000100030073-5",
        "name": "CIA_Intelligence_Report_US_Psychic_Spies_Iran",
        "desc": "CIA Intelligence Report on US deployment of psychic spies in the Iran Crisis"
    },

    # 2. Soviet Parapsychology, Psychotronics, & Robert Toth Case
    {
        "cat": "SOVIET_PARAPSYCHOLOGY_PSYCHOTRONICS",
        "id": "cia-readingroom-document-cia-rdp96-00792r000500210001-9",
        "name": "CIA_Parapsychology_in_the_USSR_Report",
        "desc": "Comprehensive CIA Intelligence Assessment: Parapsychology in the USSR (1960-1977)"
    },
    {
        "cat": "SOVIET_PARAPSYCHOLOGY_PSYCHOTRONICS",
        "id": "cia-readingroom-document-cia-rdp96-00792r000600350002-2",
        "name": "DIA_Soviet_and_Czechoslovakian_Parapsychology_Research",
        "desc": "DIA Research Report on Soviet and Czechoslovakian parapsychology/psychotronics"
    },
    {
        "cat": "SOVIET_PARAPSYCHOLOGY_PSYCHOTRONICS",
        "id": "cia-readingroom-document-cia-rdp96-00792r000600310001-7",
        "name": "DOD_Psychoenergetics_Assessment",
        "desc": "Department of Defense Assessment on Psychoenergetics and Telepathic Applications"
    },
    {
        "cat": "SOVIET_PARAPSYCHOLOGY_PSYCHOTRONICS",
        "id": "cia-readingroom-document-cia-rdp96-00792r000600070004-1",
        "name": "Use_of_ESP_for_Communication_Tested_with_US_Cooperation",
        "desc": "Intelligence study on Soviet telepathic and ESP communication experiments"
    },
    {
        "cat": "SOVIET_PARAPSYCHOLOGY_PSYCHOTRONICS",
        "id": "cia-readingroom-document-cia-rdp96-00792r000500260002-3",
        "name": "Soviet_Electronic_Devices_Modeled_After_Living_Systems",
        "desc": "Soviet electronic devices and biophysical sensor models"
    },
    {
        "cat": "SOVIET_PARAPSYCHOLOGY_PSYCHOTRONICS",
        "id": "cia-readingroom-document-cia-rdp96-00792r000500680012-6",
        "name": "Defense_News_US_Explores_Russian_Mind_Control_Tech",
        "desc": "Defense News analysis on US government inquiries into Russian mind-control technology"
    },
    {
        "cat": "SOVIET_PARAPSYCHOLOGY_PSYCHOTRONICS",
        "id": "cia-readingroom-document-cia-rdp90-00965r000504610002-7",
        "name": "For_Reporter_Toth_A_Lesson_in_Soviet_Paranoia",
        "desc": "Declassified analysis of the Robert Toth KGB interrogation over Soviet parapsychology"
    },

    # 3. Moscow Embassy Microwave Irradiation (Project Pandora)
    {
        "cat": "MOSCOW_EMBASSY_MICROWAVE_PANDORA",
        "id": "cia-readingroom-document-cia-rdp88b01125r000300120055-1",
        "name": "State_Dept_Coverup_of_Moscow_Embassy_Microwaves",
        "desc": "Intelligence dispatch on Foreign Service Officer reactions to Moscow Embassy microwave beaming"
    },
    {
        "cat": "MOSCOW_EMBASSY_MICROWAVE_PANDORA",
        "id": "cia-readingroom-document-cia-rdp90-00965r000302520002-1",
        "name": "Embassy_in_Moscow_A_Furor_Grows",
        "desc": "Intelligence compilation on microwave radiation and biological hazards in Moscow Embassy"
    },
    {
        "cat": "MOSCOW_EMBASSY_MICROWAVE_PANDORA",
        "id": "cia-readingroom-document-cia-rdp88b01125r000300120059-7",
        "name": "Phone_Line_Carries_Radiation_to_US_Embassy_Moscow",
        "desc": "Declassified report on transmission lines carrying microwave radiation to Embassy"
    },
    {
        "cat": "MOSCOW_EMBASSY_MICROWAVE_PANDORA",
        "id": "cia-readingroom-document-cia-rdp88-01315r000400270004-8",
        "name": "Embassy_Staff_Blood_Tested_in_Moscow",
        "desc": "Medical testing of US Foreign Service personnel following microwave exposure in Moscow"
    },

    # 4. Declassified UFO / UAP Intelligence Documents
    {
        "cat": "UAP_INTELLIGENCE_REPORTS",
        "id": "cia-readingroom-document-cia-rdp79b00752a000300100010-4",
        "name": "Robertson_Panel_Scientific_Advisory_Report_UFO_1953",
        "desc": "Official Report of the 1953 Robertson Scientific Advisory Panel on UFOs (CIA/OSI)"
    },
    {
        "cat": "UAP_INTELLIGENCE_REPORTS",
        "id": "cia-readingroom-document-0000015481",
        "name": "CIA_Sightings_of_Unidentified_Flying_Objects_Official_File",
        "desc": "CIA Intelligence collection on global sightings of unidentified flying objects"
    },
    {
        "cat": "UAP_INTELLIGENCE_REPORTS",
        "id": "cia-readingroom-document-0000015480",
        "name": "CIA_Sightings_of_Unidentified_Flying_Objects_Summer_1954",
        "desc": "Declassified CIA report on international UFO sightings"
    },
    {
        "cat": "UAP_INTELLIGENCE_REPORTS",
        "id": "cia-readingroom-document-cia-rdp81r00560r000100010002-9",
        "name": "CIA_Flying_Saucers_UFO_Reports_Dossier",
        "desc": "CIA master intelligence file on flying saucers and anomalous aerial phenomena"
    },
    {
        "cat": "UAP_INTELLIGENCE_REPORTS",
        "id": "cia-readingroom-document-0000042346",
        "name": "USSR_Media_Report_Multitude_of_UFO_Sightings",
        "desc": "CIA Foreign Broadcast Information Service (FBIS) report on Soviet UFO sightings"
    }
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def get_base_id(ident):
    if ident.startswith("cia-readingroom-document-"):
        return ident[len("cia-readingroom-document-"):]
    return ident

def download_file(url, dest_path, timeout=35):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = r.read()
                if len(data) > 0:
                    with open(dest_path, "wb") as f:
                        f.write(data)
                    return len(data)
        except Exception as e:
            time.sleep(1.0 * (attempt + 1))
    return 0

def process_doc(doc):
    ident = doc["id"]
    clean_name = doc["name"]
    base_id = get_base_id(ident)
    
    pdf_dest = os.path.join(PDF_DIR, f"{clean_name}.pdf")
    txt_dest = os.path.join(TXT_DIR, f"{clean_name}.txt")
    
    pdf_size = os.path.getsize(pdf_dest) if os.path.exists(pdf_dest) else 0
    txt_size = os.path.getsize(txt_dest) if os.path.exists(txt_dest) else 0
    
    # 1. Download PDF if not present
    if pdf_size == 0:
        pdf_urls = [
            f"https://archive.org/download/{ident}/{base_id}.pdf",
            f"https://archive.org/download/{ident}/{ident}.pdf",
            f"https://www.cia.gov/readingroom/docs/{base_id}.pdf"
        ]
        for purl in pdf_urls:
            s = download_file(purl, pdf_dest, timeout=40)
            if s > 0:
                pdf_size = s
                break
                
    # 2. Download TXT if not present
    if txt_size == 0:
        txt_urls = [
            f"https://archive.org/download/{ident}/{base_id}_djvu.txt",
            f"https://archive.org/download/{ident}/{base_id}.txt",
            f"https://archive.org/download/{ident}/{ident}_djvu.txt"
        ]
        for turl in txt_urls:
            s = download_file(turl, txt_dest, timeout=30)
            if s > 0:
                txt_size = s
                break
                
    status = "OK" if (pdf_size > 0 and txt_size > 0) else "PARTIAL"
    print(f"[{status}] {clean_name} -> PDF: {pdf_size:,} B | TXT: {txt_size:,} B")
    
    return {
        "category": doc["cat"],
        "name": clean_name,
        "identifier": ident,
        "description": doc["desc"],
        "pdf_path": f"pdf/{clean_name}.pdf" if pdf_size > 0 else None,
        "pdf_bytes": pdf_size,
        "txt_path": f"txt/{clean_name}.txt" if txt_size > 0 else None,
        "txt_bytes": txt_size
    }

def main():
    print(f"Starting parallel download of {len(TARGET_DOCUMENTS)} primary declassified records with 5 workers...")
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_doc, doc): doc for doc in TARGET_DOCUMENTS}
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            
    # Sort results to match original category and name order
    order_map = {doc["name"]: idx for idx, doc in enumerate(TARGET_DOCUMENTS)}
    results.sort(key=lambda x: order_map.get(x["name"], 999))
    
    # Save Manifest
    manifest_path = os.path.join(SOURCES_DIR, "MANIFEST.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved MANIFEST.json ({len(results)} records)")
    
    # Generate INDEX.md
    index_path = os.path.join(SOURCES_DIR, "INDEX.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("# Index of Declassified Primary Source Documents (PDF & Verbatim TXT)\n\n")
        f.write("**Directory:** `C:/Workspace/indonesian-govt-secrets-parapsychic/declassified_primary_sources/`  \n")
        f.write("**Total Files Cataloged:** " + str(len(results)) + " primary documents in both `.pdf` and `.txt` format.\n\n")
        f.write("---\n\n")
        
        current_cat = None
        for item in results:
            if item["category"] != current_cat:
                current_cat = item["category"]
                f.write(f"\n## Category: {current_cat.replace('_', ' ')}\n\n")
                f.write("| Document Title | Original Archive ID | PDF Size | OCR Text Size | Description |\n")
                f.write("|---|---|---|---|---|\n")
                
            pdf_str = f"[`{item['name']}.pdf`]({item['pdf_path']}) ({item['pdf_bytes']:,} B)" if item['pdf_path'] else "N/A"
            txt_str = f"[`{item['name']}.txt`]({item['txt_path']}) ({item['txt_bytes']:,} B)" if item['txt_path'] else "N/A"
            f.write(f"| **{item['name']}** | `{item['identifier']}` | {pdf_str} | {txt_str} | {item['description']} |\n")

    print(f"Generated INDEX.md at {index_path}")

if __name__ == "__main__":
    main()
