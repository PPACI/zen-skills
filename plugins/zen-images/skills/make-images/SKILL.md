---
name: make-images
description: Use when generating or editing images through the OpenRouter API, choosing an image model, building multi-reference prompts, cleaning up photos of objects for listings, producing a realistic portrait of a real person from photos, drawing a cartoon of a real person, making a sticker pack, or producing an SVG (vector) illustration.
---

# Make images

Observed 2026-10-17, 2026-11-07 and 2026-11-13 through live API calls. Model names, parameters, and prices change; list models before relying on any of this.

## Models

List image-capable models with `GET https://openrouter.ai/api/v1/models?output_modalities=image`. The plain `/models` list omits several image models.

## Balance

Any image or video output returns HTTP 402 "requires at least $1.00 in balance" when the account balance is under $1, whatever the model and the image's own price. Check `GET /api/v1/credits` (`total_credits - total_usage`) before a batch. A key's own usage covers that key only; the balance counts every key on the account.

## Endpoints

| Model family | Endpoint | Request | Output |
| --- | --- | --- | --- |
| Gemini image (`google/gemini-*-image`, nano-banana) | `POST /api/v1/chat/completions` | `modalities: ["image","text"]`, `image_config.aspect_ratio`; references as image parts | `choices[0].message.images[0].image_url.url` (data URL) |
| FLUX, OpenAI GPT Image, Recraft | `POST /api/v1/images` (chat returns 404) | `model`, `prompt`, `input_references: [{type:"image_url", image_url:{url}}]` | `data[0].b64_json` (an SVG document for Recraft `*-vector` models) |

## Parameter pitfalls (HTTP 400)

- FLUX rejects `quality` and `output_format` (returns PNG).
- GPT Image accepts aspect ratios 1:1, 3:2, 2:3, 4:3, 3:4, 16:9, 9:16, 21:9; not 4:5.
- For high resolution on GPT Image, pass explicit pixels (`size: "2304x3072"`); tier strings such as `"2K"` are rejected.
- Gemini Pro accepts `image_config.image_size: "2K"`.
- Recraft accepts at most one `input_references` item.
- Phone photos often store rotation only in the EXIF orientation tag; send pixels already upright, or the model may receive the image sideways.

## Observed cost per image

nano-banana-2.1 about $0.04; flux-3 2K about $0.10; gpt-image-2 high about $0.21; gpt-image-2.5 at 2304x3072 about $0.49; gpt-image-2.6 high at 1152x1536 about $0.06-0.09 (more with extra references), at 3072x2304 about $0.15; recraft-v4.1-vector about $0.08.

## Portrait of a real person

- Send several references: image 1 a style reference marked "do NOT copy the face", then 2-3 identity crops of the real face.
- Specify the relight explicitly: neutral white balance (~5500K), key/fill/hair light, wardrobe cleanup, framing.
- Identity fidelity observed: GPT Image closest, FLUX close but restyles hair, nano-banana may change eye and hair colour. Check each output for identity drift.
- Prefer native high resolution over upscaling. If upscaling, Real-ESRGAN x4 alone makes skin waxy; blend 50/50 with a Lanczos x4 resize and add fine luminance grain.

## Cleaning up a photo of an object

For product or second-hand listing photos: remove clutter, plain wall and floor, keep the object faithful.

- Name what to keep: the object's exact configuration (count of parts, proportions, colour, finish), and list what to remove.
- Without references for its surfaces, GPT Image invented wear marks on a clean top. Pass close-ups of those surfaces as extra references ("images after the first one are close-ups of the same object: copy that finish").
- To show a real defect, edit a close-up of it and say "keep the chip exactly as it is (same position, size, colour)"; GPT Image kept it while removing everything around.
- Compare every output with the real photos before using it.

## Cartoon of a real person

- GPT Image with 2-3 face crops as references kept the likeness in flat cartoon and chibi styles, and spelled short captions correctly.
- To reuse a design the user liked, pass it as image 1 ("keep this style and layout") and the face crops after it.

## SVG (vector) output

- Recraft `*-vector` models return a real SVG. Given a photo as reference, they produced a messy semi-photographic trace. Draw the cartoon with GPT Image first, then pass that PNG as Recraft's only reference: "redraw this exact image as a flat vector illustration".
- Recraft redraws freely: it misspelled captions, turned closed eyes into an odd side-glance, and changed skin and clothing colours. List every caption verbatim in the prompt, describe key features explicitly ("eyes fully closed, no pupils"), run 2-3 tries, and render each to read its text before delivering.
- Fix colours in the SVG itself: fills are `rgb(...)` literals. When the colour is shared with other elements, select the paths by the bounding box of their `d` coordinates. Remove `preserveAspectRatio="none"`.

## Sticker pack

- Generate all stickers on one GPT Image sheet (4x3 at `size: "3072x2304"`): one sheet keeps the character consistent across stickers. Ask for die-cut stickers whose white border encloses the drawing and its caption.
- GPT Image 2.6 returned a transparent RGBA background for a sticker sheet even when asked for a solid colour. Check the alpha channel before keying; previews show the hidden colour under transparent pixels as a grey blotchy pattern.
- To change captions or language, pass the previous sheet (flattened on a solid colour) as image 1 with "reproduce this exact sheet, only change the captions": the drawings stayed the same.
- Slice by connected components of the alpha mask (each white border keeps one sticker in one piece), pad to square, resize to 512x512. WhatsApp wants WebP under 100 KB per sticker and a 96x96 tray icon; WebP quality 90 gave 40-70 KB.
