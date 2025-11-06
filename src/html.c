#include "html.h"
#include <string.h>
#include <ctype.h>
#include <stdio.h>

static SDL_Color BLACK = {0,0,0,255};

static void add_text(ReDocument* d, const char* s, ReStyle st) {
  if (!s || !*s) return;
  if (d->count >= RE_MAX_ELEMENTS) return;
  ReElement* e = &d->elems[d->count++];
  e->type = RE_E_TEXT;
  e->style = st;
  e->tex = NULL;
  strncpy(e->text, s, sizeof(e->text)-1);
}

static void add_img(ReDocument* d, const char* url) {
  if (d->count >= RE_MAX_ELEMENTS) return;
  ReElement* e = &d->elems[d->count++];
  e->type = RE_E_IMG;
  e->tex = NULL;
  e->img_w = e->img_h = 0;
  strncpy(e->src, url, sizeof(e->src)-1);
}

static void trim(char* s) {
  if (!s) return;
  size_t n = strlen(s);
  while (n && isspace((unsigned char)s[n-1])) s[--n] = 0;
  size_t i = 0;
  while (s[i] && isspace((unsigned char)s[i])) i++;
  if (i) memmove(s, s+i, strlen(s+i)+1);
}

void re_parse_html(const char* html, ReDocument* out) {
  memset(out, 0, sizeof(*out));
  if (!html) return;
  ReStyle st = {0};
  st.color = BLACK;

  const char* p = html;
  char buf[2048];
  while (*p && out->count < RE_MAX_ELEMENTS) {
    if (*p == '<') {
      if (!strncasecmp(p, "<h1>", 4)) { st.h1 = 1; p += 4; continue; }
      else if (!strncasecmp(p, "</h1>", 5)) { st.h1 = 0; p += 5; continue; }
      else if (!strncasecmp(p, "<b>", 3)) { st.bold = 1; p += 3; continue; }
      else if (!strncasecmp(p, "</b>", 4)) { st.bold = 0; p += 4; continue; }
      else if (!strncasecmp(p, "<i>", 3)) { st.italic = 1; p += 3; continue; }
      else if (!strncasecmp(p, "</i>", 4)) { st.italic = 0; p += 4; continue; }
      else if (!strncasecmp(p, "<p>", 3)) { add_text(out, "\n", st); p += 3; continue; }
      else if (!strncasecmp(p, "<br>", 4) || !strncasecmp(p, "<br/>", 5)) {
        add_text(out, "\n", st);
        p += (*p=='<' && *(p+3)=='>') ? 4 : 5;
        continue;
      } else if (!strncasecmp(p, "<img", 4)) {
        const char* q = strstr(p, "src=");
        if (q) {
          q += 4;
          if (*q=='\"' || *q=='\'') {
            char quote = *q++;
            const char* end = strchr(q, quote);
            if (end) {
              size_t len = (size_t)(end - q);
              if (len >= sizeof(buf)) len = sizeof(buf)-1;
              strncpy(buf, q, len); buf[len] = 0;
              trim(buf);
              add_img(out, buf);
            }
          }
        }
        const char* r = strchr(p, '>');
        p = r ? r+1 : p+1;
        continue;
      } else {
        const char* r = strchr(p, '>');
        p = r ? r+1 : p+1;
        continue;
      }
    } else {
      const char* r = strchr(p, '<');
      size_t len = r ? (size_t)(r - p) : strlen(p);
      if (len >= sizeof(buf)) len = sizeof(buf)-1;
      strncpy(buf, p, len); buf[len] = 0;
      trim(buf);
      if (*buf) add_text(out, buf, st);
      p += len;
    }
  }
}
