# Nano Banana — Gemini Image Generation API Docs

Nano Banana is Google's name for Gemini's native image generation capabilities. Gemini can generate and process images conversationally with text, images, or a combination of both.

---

## Models

| Nickname        | Model ID                         | Best For                                                       |
| --------------- | -------------------------------- | -------------------------------------------------------------- |
| Nano Banana     | `gemini-2.5-flash-image`         | Speed, high-volume, low-latency                                |
| Nano Banana 2   | `gemini-3.1-flash-image-preview` | Best all-around: performance, intelligence, cost, latency      |
| Nano Banana Pro | `gemini-3-pro-image-preview`     | Professional asset production, complex instructions, 4K output |

All generated images include a **SynthID watermark**.

---

## What's New in Gemini 3 Image Models

- **High-resolution output**: 512, 1K, 2K, 4K (Pro only: 4K; Flash adds 512)
- **Advanced text rendering**: Legible, stylized text for infographics, menus, marketing assets
- **Grounding with Google Search**: Generate images based on real-time data (weather, events, stock charts)
- **Image Search grounding** _(3.1 Flash only)_: Use web images as visual context
- **Thinking mode**: Reasoning process enabled by default; generates interim "thought images" to refine composition
- **Up to 14 reference images**: Mix objects + characters for high-fidelity output
- **New aspect ratios** _(3.1 Flash)_: 1:4, 4:1, 1:8, 8:1

---

## Reference Image Limits

| Type                   | Nano Banana 2 (3.1 Flash) | Nano Banana Pro (3 Pro) |
| ---------------------- | ------------------------- | ----------------------- |
| High-fidelity objects  | Up to 10                  | Up to 6                 |
| Character consistency  | Up to 4 characters        | Up to 5 characters      |
| Total reference images | Up to 14                  | Up to 14                |

> `gemini-2.5-flash-image` works best with up to 3 input images.

---

## Aspect Ratios & Resolutions

### Nano Banana 2 — `gemini-3.1-flash-image-preview`

| Aspect Ratio | 512 (0.5K) | 1K        | 2K        | 4K         |
| ------------ | ---------- | --------- | --------- | ---------- |
| 1:1          | 512×512    | 1024×1024 | 2048×2048 | 4096×4096  |
| 16:9         | 688×384    | 1376×768  | 2752×1536 | 5504×3072  |
| 9:16         | 384×688    | 768×1376  | 1536×2752 | 3072×5504  |
| 3:2          | 632×424    | 1264×848  | 2528×1696 | 5056×3392  |
| 2:3          | 424×632    | 848×1264  | 1696×2528 | 3392×5056  |
| 4:3          | 600×448    | 1200×896  | 2400×1792 | 4800×3584  |
| 3:4          | 448×600    | 896×1200  | 1792×2400 | 3584×4800  |
| 4:1          | 1024×256   | 2048×512  | 4096×1024 | 8192×2048  |
| 1:4          | 256×1024   | 512×2048  | 1024×4096 | 2048×8192  |
| 1:8          | 192×1536   | 384×3072  | 768×6144  | 1536×12288 |
| 8:1          | 1536×192   | 3072×384  | 6144×768  | 12288×1536 |
| 21:9         | 792×168    | 1584×672  | 3168×1344 | 6336×2688  |

> Use uppercase `K` (e.g. `1K`, `2K`, `4K`). Lowercase will be rejected. `512` has no `K` suffix.

### Nano Banana Pro — `gemini-3-pro-image-preview`

Supports 1K, 2K, 4K. Does **not** support 512. Same aspect ratios except 1:4, 4:1, 1:8, 8:1 (Flash only).

### Nano Banana — `gemini-2.5-flash-image`

Generates at 1024px (1K) only. Aspect ratio configurable.

---

## Code Examples

### 1. Text-to-Image (Basic)

```python
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()

prompt = "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[prompt],
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        image.save("generated_image.png")
```

---

### 2. Image Editing (Text + Image → Image)

```python
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()

prompt = (
    "Create a picture of my cat eating a nano-banana in a "
    "fancy restaurant under the Gemini constellation"
)

image = Image.open("/path/to/cat_image.png")

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[prompt, image],
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        image.save("generated_image.png")
```

---

### 3. Multi-Turn Image Editing (Chat)

```python
from google import genai
from google.genai import types

client = genai.Client()

chat = client.chats.create(
    model="gemini-3.1-flash-image-preview",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        tools=[{"google_search": {}}]
    )
)

message = "Create a vibrant infographic that explains photosynthesis as if it were a recipe for a plant's favorite food."

response = chat.send_message(message)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif image := part.as_image():
        image.save("photosynthesis.png")
```

Follow-up edit in the same chat:

```python
message = "Update this infographic to be in Spanish. Do not change any other elements of the image."
aspect_ratio = "16:9"  # "1:1","1:4","1:8","2:3","3:2","3:4","4:1","4:3","4:5","5:4","8:1","9:16","16:9","21:9"
resolution = "2K"      # "512", "1K", "2K", "4K"

response = chat.send_message(
    message,
    config=types.GenerateContentConfig(
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=resolution
        ),
    )
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif image := part.as_image():
        image.save("photosynthesis_spanish.png")
```

---

### 4. Multiple Reference Images

```python
from google import genai
from google.genai import types
from PIL import Image

prompt = "An office group photo of these people, they are making funny faces."
aspect_ratio = "5:4"
resolution = "2K"

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[
        prompt,
        Image.open('person1.png'),
        Image.open('person2.png'),
        Image.open('person3.png'),
        Image.open('person4.png'),
        Image.open('person5.png'),
    ],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=resolution
        ),
    )
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif image := part.as_image():
        image.save("office.png")
```

---

### 5. Grounding with Google Search (Web)

```python
from google import genai

prompt = "Visualize the current weather forecast for the next 5 days in San Francisco as a clean, modern weather chart. Add a visual on what I should wear each day"
aspect_ratio = "16:9"

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=['Text', 'Image'],
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
        ),
        tools=[{"google_search": {}}]
    )
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif image := part.as_image():
        image.save("weather.png")
```

The response includes `groundingMetadata` with:

- `searchEntryPoint`: HTML/CSS to render required search suggestions
- `groundingChunks`: Top 3 web sources used to ground the image

---

### 6. Grounding with Google Image Search _(3.1 Flash only)_

```python
from google import genai
from google.genai import types

prompt = "A detailed painting of a Timareta butterfly resting on a flower"

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        tools=[
            types.Tool(google_search=types.GoogleSearch(
                search_types=types.SearchTypes(
                    web_search=types.WebSearch(),
                    image_search=types.ImageSearch()
                )
            ))
        ]
    )
)
```

> **Display requirements**: You must provide a link to the source webpage (not the image file directly). Single-click path from image to source page is required. No intermediate viewers.

`groundingMetadata` for image search includes:

- `imageSearchQueries`: Queries used for visual context
- `groundingChunks[].uri`: Source webpage URL for attribution
- `groundingChunks[].image_uri`: Direct image URL
- `searchEntryPoint`: Google Search chip HTML/CSS

---

### 7. Custom Resolution & Aspect Ratio

```python
from google import genai
from google.genai import types

prompt = "Da Vinci style anatomical sketch of a dissected Monarch butterfly."
aspect_ratio = "1:1"  # "1:1","1:4","1:8","2:3","3:2","3:4","4:1","4:3","4:5","5:4","8:1","9:16","16:9","21:9"
resolution = "4K"     # "512", "1K", "2K", "4K"

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=resolution
        ),
    )
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif image := part.as_image():
        image.save("butterfly.png")
```

---

### 8. Thinking Mode & Thought Inspection

Thinking is **enabled by default** and cannot be disabled. The model generates up to 2 interim "thought images" to refine composition. Thought tokens are billed regardless of `include_thoughts`.

```python
from google import genai
from google.genai import types

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents="A futuristic city built inside a giant glass bottle floating in space",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        thinking_config=types.ThinkingConfig(
            thinking_level="High",   # "minimal" (default) or "high"
            include_thoughts=True
        ),
    )
)

for part in response.parts:
    if part.thought:  # skip thought images
        continue
    if part.text:
        print(part.text)
    elif image := part.as_image():
        image.show()
```

To inspect thoughts:

```python
for part in response.parts:
    if part.thought:
        if part.text:
            print(part.text)
        elif image := part.as_image():
            image.show()
```

---

### 9. Image-Only Output

```python
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=['Image']
    )
)
```

---

### 10. Batch Generation

For high-volume generation, use the Batch API. Higher rate limits in exchange for up to 24-hour turnaround.

```python
# See: https://ai.google.dev/gemini-api/docs/batch
# Batch API supports image generation with the same model IDs
```

---

## Thinking — Thought Signatures

Thought signatures are encrypted representations of the model's reasoning, used to preserve context across multi-turn interactions. Pass them back exactly as received.

> If you use the official Google Gen AI SDK with the chat feature, thought signatures are handled automatically.

**Rules:**

- All `inline_data` image parts in the response have a `thought_signature`
- The first non-thought text part (after thoughts) has a `thought_signature`
- Thought images themselves do NOT have signatures
- Subsequent text parts after the first do NOT have signatures

---

## Prompting Strategies

### 1. Photorealistic Scenes

```
A photorealistic [shot type] of [subject], [action or expression], set in [environment].
The scene is illuminated by [lighting description], creating a [mood] atmosphere.
Captured with a [camera/lens details], emphasizing [key textures and details].
The image should be in a [aspect ratio] format.
```

### 2. Stylized Illustrations & Stickers

```
A [style] sticker of a [subject], featuring [key characteristics] and a [color palette].
The design should have [line style] and [shading style]. The background must be white.
```

> The model does not support transparent backgrounds.

### 3. Accurate Text in Images

```
Create a [image type] for [brand/concept] with the text "[text to render]" in a [font style].
The design should be [style description], with a [color scheme].
```

> Use `gemini-3-pro-image-preview` for professional text rendering.

### 4. Product Mockups

```
A high-resolution, studio-lit product photograph of a [product] on a [background].
The lighting is a [lighting setup] to [purpose]. The camera angle is a [angle] to showcase [feature].
Ultra-realistic, with sharp focus on [key detail]. [Aspect ratio].
```

### 5. Minimalist / Negative Space

```
A minimalist composition featuring a single [subject] positioned in the [corner] of the frame.
The background is a vast, empty [color] canvas. Soft, subtle lighting. [Aspect ratio].
```

### 6. Sequential Art / Comic Panels

```
Make a 3 panel comic in a [style]. Put the character in a [type of scene].
```

> Best with `gemini-3-pro-image-preview` or `gemini-3.1-flash-image-preview`.

### 7. Grounding with Google Search

```
Make a simple but stylish graphic of last night's Arsenal game in the Champion's League
```

### Editing Prompts

| Use Case            | Template                                                                                                                                                 |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Add/remove elements | `Using the provided image of [subject], please [add/remove] [element]. Ensure the change [integrates naturally].`                                        |
| Inpainting          | `Using the provided image, change only the [element] to [new]. Keep everything else exactly the same.`                                                   |
| Style transfer      | `Transform the provided photograph of [subject] into the artistic style of [artist]. Preserve the composition but render with [stylistic elements].`     |
| Composite           | `Create a new image combining elements from the provided images. Take [element 1] and place it with [element 2]. Final image should be [description].`   |
| Detail preservation | `Using the provided images, place [element from image 2] onto [element from image 1]. Ensure features of [image 1 element] remain completely unchanged.` |
| Sketch to photo     | `Turn this rough [medium] sketch of a [subject] into a [style] photo. Keep [specific features] but add [new details].`                                   |

---

## Best Practices

- **Be hyper-specific**: "ornate elven plate armor, etched with silver leaf patterns" beats "fantasy armor"
- **Provide intent**: "logo for a high-end minimalist skincare brand" beats "create a logo"
- **Iterate conversationally**: Use chat to refine — "make the lighting warmer", "keep everything but change the expression"
- **Step-by-step for complex scenes**: Break into stages — background first, then foreground, then details
- **Semantic negative prompts**: Say what you want, not what you don't — "empty street with no signs of traffic" beats "no cars"
- **Use photography language**: wide-angle, macro, low-angle, three-point softbox, golden hour
- **Generate text first**: For images with text, generate the text content first, then request the image

---

## Limitations

- Supported languages: EN, ar-EG, de-DE, es-MX, fr-FR, hi-IN, id-ID, it-IT, ja-JP, ko-KR, pt-BR, ru-RU, ua-UA, vi-VN, zh-CN
- No audio or video inputs
- Model may not always produce the exact number of images requested
- `gemini-2.5-flash-image`: best with up to 3 input images
- `gemini-3-pro-image-preview`: up to 5 high-fidelity images, 14 total
- `gemini-3.1-flash-image-preview`: up to 4 character references, 10 high-fidelity objects
- Image Search grounding cannot search for real-world images of people
- All outputs include SynthID watermark

---

## When to Use Imagen Instead

Imagen 4 is Google's specialized image generation model, also available via the Gemini API. Use it when:

- You need the absolute best image quality (use **Imagen 4 Ultra** — generates 1 image at a time)
- You don't need conversational/multi-turn editing
- You don't need text+image interleaving

---

## Pricing Summary

| Model                                             | Cost / Image |
| ------------------------------------------------- | ------------ |
| Nano Banana (`gemini-2.5-flash-image`)            | ~$0.038      |
| Nano Banana 2 (`gemini-3.1-flash-image-preview`)  | ~$0.01–0.02  |
| Nano Banana Pro 2K (`gemini-3-pro-image-preview`) | ~$0.14       |
| Nano Banana Pro 4K (`gemini-3-pro-image-preview`) | ~$0.24       |

> Thinking tokens are always billed, even when `include_thoughts=False`.
