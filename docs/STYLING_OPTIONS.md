# Presentation Styling Options

This document describes all available styling options for customizing presentations in the SlideGenerator application.

## Overview

The styling system allows you to customize the visual appearance of presentations without changing their content. You can:

- Apply predefined themes
- Set custom colors for various elements
- Change fonts
- Apply other visual modifications

## How to Apply Styles

Styles can be applied to an existing presentation using the API endpoint:

```
POST /api/v1/presentations/{presentation_id}/configure-style
```

Example request body:

```json
{
  "theme": "corporate",
  "background_color": "#F5F5F5",
  "font": "Arial",
  "title_color": "#003366",
  "content_color": "#333333",
  "accent_color": "#FF6600"
}
```

## Available Options

### Themes

The `theme` parameter sets a predefined visual style:

| Theme Name | Description |
|------------|-------------|
| `professional` | Default business theme with blue tones |
| `corporate` | Conservative corporate style with dark blue and orange accents |
| `creative` | Bold and vibrant style with red and orange tones |
| `academic` | Scholarly style with maroon and gold tones |
| `dark` | Dark background with light text for low-light environments |
| `minimal` | Clean, minimalist style with muted colors |
| `modern startup` | Contemporary style with bright blue and orange |
| `youthful` | Playful style with purple, blue and green tones |

### Colors

You can customize specific colors using hex color codes:

| Parameter | Description | Default (Professional Theme) |
|-----------|-------------|------------------------------|
| `background_color` | Slide background color | `#FFFFFF` (white) |
| `title_color` | Title text color | `#1F497D` (dark blue) |
| `content_color` | Content/body text color | `#444444` (dark gray) |
| `accent_color` | Color for highlights and accents | `#ED7D31` (orange) |

Example:
```json
{
  "background_color": "#F0F8FF",
  "title_color": "#800000"
}
```

### Fonts

The `font` parameter allows you to set the font family for the presentation:

```json
{
  "font": "Helvetica"
}
```

Common fonts that work well in PowerPoint:
- Arial
- Calibri (default)
- Helvetica
- Times New Roman
- Georgia
- Verdana
- Tahoma
- Trebuchet MS

## Style Storage and Database Handling

When applying styles through the API, the entire style configuration is stored in the database as a JSON object in the `style_config` column. Each style update completely replaces the previous configuration rather than merging with it.

This means:
1. When applying a new style, you must include all desired properties
2. Any properties not included will revert to defaults
3. You can view the current style configuration in the presentation API response

Example database representation:
```json
{
  "theme": "corporate",
  "background_color": "#F5F5F5",
  "font": "Arial", 
  "title_color": "#003366",
  "content_color": "#333333",
  "accent_color": "#FF6600"
}
```

## Advanced Usage

### Combining Options

You can combine multiple styling options in a single request:

```json
{
  "theme": "professional",
  "background_color": "#F0F0F0",
  "font": "Georgia"
}
```

### Incremental Updates

You can update only specific aspects of the styling without changing others. For example, to change just the font:

```json
{
  "font": "Georgia"
}
```

### Dark Mode Styling

For dark mode presentations, use dark backgrounds with light text:

```json
{
  "theme": "dark",
  "background_color": "#121212",
  "title_color": "#BB86FC",
  "content_color": "#E0E0E0"
}
```

## Best Practices

1. **Color Contrast**: Ensure sufficient contrast between text and background colors for readability.
2. **Consistency**: Use a consistent color palette throughout the presentation.
3. **Font Selection**: Choose professional fonts appropriate for your audience.
4. **Testing**: Preview your presentation on different devices to ensure it looks good in various contexts. 