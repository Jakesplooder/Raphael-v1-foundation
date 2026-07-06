# POD Generation Request PODGEN-4C84E8FE10

## Request ID

PODGEN-4C84E8FE10

## Concept ID

PODCON-FB04B5A340

## Model

sdxl

## Prompt

Christian outdoors mountain cross shirt, Vintage badge illustration, screen-print friendly, centered composition, limited colors, distressed texture., Charcoal, Cream, Muted gold, Forest green, Rust, original artwork, centered t-shirt graphic, crisp silhouette, print-ready composition, professional vector-inspired illustration

## Negative Prompt

mockup, garment, person, watermark, logo, copyrighted character, trademark, brand name, blurry, low contrast, tiny details, photo background, illegible text, extra text, artifacts

## Width

1024

## Height

1024

## Steps

30

## CFG / Guidance

7.0

## Number of Variants

4

## Output Folder

C:\RaphaelOS\PODStudio\generated\PODGEN-4C84E8FE10

## ComfyUI Workflow JSON

C:\RaphaelOS\PODStudio\templates\PODGEN-4C84E8FE10 - ComfyUI API Workflow.json

## Safety Notes

- Pending requests do not generate images.
- Local ComfyUI is the only permitted generation target.
- No Etsy, Printify, credential, publishing, upload, spending, or external API action is authorized.
- The workflow remains inactive until Aaron confirms local generation.

## Status

Approved

## Suggested Next Command

`python raphael.py pod-generate "PODGEN-4C84E8FE10"`

## Generation Result

ComfyUI is reachable and checkpoint `sd_xl_base_1.0.safetensors` is available.

Raphael prepared the safe API workflow at `C:\RaphaelOS\PODStudio\templates\PODGEN-4C84E8FE10 - ComfyUI API Workflow.json` but did not queue it because ComfyUI currently writes generated files outside `C:/RaphaelOS/PODStudio/`.

Manual safe path:
1. Import the workflow JSON into local ComfyUI.
2. Configure ComfyUI output to `C:/RaphaelOS/PODStudio/generated/PODGEN-4C84E8FE10/`.
3. Run locally.
4. Use `python raphael.py pod-review-batch "C:/RaphaelOS/PODStudio/generated/PODGEN-4C84E8FE10"`.
