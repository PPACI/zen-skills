---
name: make-images
description: Use when generating or editing images through the OpenRouter API, choosing an image model, building multi-reference prompts, cleaning up photos of objects for listings, or producing a realistic portrait of a real person from photos.
---

# Make images

Observed 2026-10-17 and 2026-11-07 through live API calls. Model names, parameters, and prices change; list models before relying on any of this.

## Models

List image-capable models with `GET https://openrouter.ai/api/v1/models?output_modalities=image`. The plain `/models` list omits several image models.

## Balance

Any image or video output returns HTTP 402 "requires at least $1.00 in balance" when the account balance is under $1, whatever the model and the image's own price. Check `GET /api/v1/credits` (`total_credits - total_usage`) before a batch. A key's own usage covers that key only; the balance counts every key on the account.

## Endpoints

| Model family | Endpoint | Request | Output |
| --- | --- | --- | --- |
| Gemini image (`google/gemini-*-image`, nano-banana) | `POST /api/v1/chat/completions` | `modalities: ["image","text"]`, `image_config.aspect_ratio`; references as image parts | `choices[0].message.images[0].image_url.url` (data URL) |
| FLUX, OpenAI GPT Image | `POST /api/v1/images` (chat returns 404) | `model`, `prompt`, `input_references: [{type:"image_url", image_url:{url}}]` | `data[0].b64_json` |

## Parameter pitfalls (HTTP 400)

- FLUX rejects `quality` and `output_format` (returns PNG).
- GPT Image accepts aspect ratios 1:1, 3:2, 2:3, 4:3, 3:4, 16:9, 9:16, 21:9; not 4:5.
- For high resolution on GPT Image, pass explicit pixels (`size: "2304x3072"`); tier strings such as `"2K"` are rejected.
- Gemini Pro accepts `image_config.image_size: "2K"`.
- Phone photos often store rotation only in the EXIF orientation tag; send pixels already upright, or the model may receive the image sideways.

## Observed cost per image

nano-banana-2.1 about $0.04; flux-3 2K about $0.10; gpt-image-2 high about $0.21; gpt-image-2.5 at 2304x3072 about $0.49; gpt-image-2.6 high at 1152x1536 about $0.06-0.09 (more with extra references).

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
