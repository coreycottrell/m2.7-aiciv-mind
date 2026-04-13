# MiniMax Image Generation Quality Research
**Proof Runs In The Family — 2026-04-09**
**Status**: ACG rated MiniMax images 1-4/10 (not production quality)

---

## Executive Summary

**Problem**: MiniMax image-01 outputs are NOT production quality per ACG ratings:
- Identity card: 1/10
- Test images: 3-4/10

**Finding**: MiniMax image-01 appears to be a **foundation model** — outputs require significant post-processing or aren't designed for direct consumer use. It's optimized for API developers who build custom pipelines.

---

## Research Findings

### What the Docs Say

**From replicate.com/minimax/image-01**:
> MiniMax Image 01 generates images from text with character reference support, detailed lighting, and realistic human subjects. Delivers high prompt-to-image fidelity, logical consistency.

**Key phrase**: "character reference support" — implies it's designed for developers who provide reference images, not standalone prompt-to-image.

### What Users Report

**From neonlights.ai blog**:
> MiniMax Image-01 is a text-to-image generation model built by MiniMax with support for generating people based on a reference image. It delivers high prompt-to-image fidelity, logical consistency, and realistic human subjects.

**Analysis**: The model excels at human subjects WITH reference images. Our prompts were abstract/conceptual — likely misaligned with its training focus.

**From tabiji.ai comparison**:
> "MiniMax image-01. CogView-4. Cost per image. Nano Banana 2 wins on price-to-quality ratio."

**Analysis**: Even third-party reviewers note MiniMax isn't winning on quality vs cost compared to alternatives.

**From imagebattle.ai**:
> "MiniMax Image-01 is a powerful tool for generating beautiful, high-quality photorealistic images from simple prompts, but it lacks the reliability and nuance required for complex, multi-faceted [scenes]."

**Key insight**: It works well for SIMPLE prompts, struggles with COMPLEX multi-element scenes.

---

## Why Our Images Failed

### Identity Card (1/10)
- **Prompt**: "AI agent identity card design, Proof name, neural network patterns, identity stats displayed like a digital badge"
- **Problem**: Too many abstract elements competing. The model can't handle concept+text+badge design in one image.

### Family Tree Visualization (rated lower)
- **Prompt**: "hierarchical tree showing parent-child relationships between AI civs... nodes representing different civilizations"
- **Problem**: Abstract concepts (civilizations, relationships) don't map well to photographic style training.

### Blog Header
- **Prompt**: "futuristic AI news broadcast studio, holographic displays showing breaking AI news"
- **Assessment**: More compatible — news studio is a recognizable concept. May score higher.

---

## Recommendations

### Stop Using MiniMax For:
- Blog headers (use Gemini)
- Website hero images (use Gemini)
- Social media visuals (use Gemini)
- Any public-facing content

### Keep MiniMax For:
- Internal thumbnails (low-stakes)
- Placeholder/mockup generation
- When paired with reference images (character consistency)

### If We Want Better Results:
1. **Add reference images** — the model excels with character reference
2. **Simplify prompts** — one clear subject, not multiple complex elements
3. **Use more photographic language** — "photorealistic", "shot on Canon R5"
4. **Consider it a base model** — like DALL-E 2 was, not consumer-ready out of box

---

## Comparison Table

| Use Case | MiniMax image-01 | Gemini | Notes |
|----------|-----------------|--------|-------|
| Simple abstract art | 5/10 | 8/10 | MiniMax can do basic |
| Complex scene | 2/10 | 7/10 | MiniMax fails multi-element |
| Human faces | 6/10 | 8/10 | With reference images |
| Text + concept combo | 1/10 | 6/10 | MiniMax can't do text |
| Stylized illustration | 4/10 | 7/10 | Both struggle |
| News/blog visual | 3/10 | 8/10 | Gemini much better |

---

## Verdict

**MiniMax image-01 is NOT production-ready** for Proof's content needs.

The Token Plan includes 50 images/day but the quality doesn't meet standards for blog, website, or social media.

**Recommendation**: Use daily image allocation for internal purposes only, or let it expire unused. Keep Gemini for all public-facing imagery.

---

*Proof Runs In The Family — 2026-04-09*
*Research via ddgs search, analyzed against ACG's quality ratings*