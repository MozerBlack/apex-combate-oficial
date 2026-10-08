package br.com.apexcombate.app;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.content.res.ColorStateList;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.CookieManager;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

public final class MainActivity extends Activity {
    private static final String APP_URL = "https://apex-combate-demo.onrender.com/apex-combate.html?v=44&source=apk";
    private static final String APP_HOST = "apex-combate-demo.onrender.com";
    private static final int FILE_CHOOSER_REQUEST = 4401;
    private static final int BACKGROUND = Color.rgb(8, 10, 14);
    private static final int SURFACE = Color.rgb(14, 18, 24);
    private static final int ACCENT = Color.rgb(239, 38, 54);
    private static final int TEXT = Color.rgb(246, 247, 249);
    private static final int MUTED = Color.rgb(146, 153, 166);

    private WebView webView;
    private View splashView;
    private View offlineView;
    private ValueCallback<Uri[]> fileChooserCallback;
    private boolean mainFrameFailed;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setStatusBarColor(BACKGROUND);
        getWindow().setNavigationBarColor(BACKGROUND);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            getWindow().getDecorView().setSystemUiVisibility(0);
        }

        FrameLayout root = new FrameLayout(this);
        root.setBackgroundColor(BACKGROUND);

        webView = new WebView(this);
        webView.setBackgroundColor(BACKGROUND);
        root.addView(webView, matchParent());

        splashView = createSplashView();
        root.addView(splashView, matchParent());

        offlineView = createOfflineView();
        offlineView.setVisibility(View.GONE);
        root.addView(offlineView, matchParent());

        setContentView(root);
        configureWebView();

        if (savedInstanceState == null || webView.restoreState(savedInstanceState) == null) {
            webView.loadUrl(APP_URL);
        }
    }

    private void configureWebView() {
        WebView.setWebContentsDebuggingEnabled(false);
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setLoadsImagesAutomatically(true);
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);
        settings.setSupportZoom(false);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setMediaPlaybackRequiresUserGesture(true);
        settings.setCacheMode(WebSettings.LOAD_DEFAULT);
        settings.setUserAgentString(settings.getUserAgentString() + " ApexCombateAndroid/44");
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            settings.setSafeBrowsingEnabled(true);
            webView.setRendererPriorityPolicy(WebView.RENDERER_PRIORITY_BOUND, false);
        }

        CookieManager cookies = CookieManager.getInstance();
        cookies.setAcceptCookie(true);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            cookies.setAcceptThirdPartyCookies(webView, false);
        }

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageStarted(WebView view, String url, Bitmap favicon) {
                super.onPageStarted(view, url, favicon);
                mainFrameFailed = false;
                offlineView.setVisibility(View.GONE);
                splashView.setVisibility(View.VISIBLE);
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                if (!mainFrameFailed) {
                    splashView.animate().alpha(0f).setDuration(220).withEndAction(new Runnable() {
                        @Override
                        public void run() {
                            splashView.setVisibility(View.GONE);
                            splashView.setAlpha(1f);
                        }
                    }).start();
                }
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
                super.onReceivedError(view, request, error);
                if (request.isForMainFrame()) showOffline();
            }

            @Override
            public void onReceivedHttpError(WebView view, WebResourceRequest request, WebResourceResponse errorResponse) {
                super.onReceivedHttpError(view, request, errorResponse);
                if (request.isForMainFrame() && errorResponse.getStatusCode() >= 500) showOffline();
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                return handleNavigation(request.getUrl());
            }

            @SuppressWarnings("deprecation")
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                return handleNavigation(Uri.parse(url));
            }
        });

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> callback, FileChooserParams params) {
                if (fileChooserCallback != null) fileChooserCallback.onReceiveValue(null);
                fileChooserCallback = callback;
                try {
                    startActivityForResult(params.createIntent(), FILE_CHOOSER_REQUEST);
                    return true;
                } catch (ActivityNotFoundException error) {
                    fileChooserCallback = null;
                    Toast.makeText(MainActivity.this, "Nenhum seletor de arquivo disponível.", Toast.LENGTH_LONG).show();
                    return false;
                }
            }
        });
    }

    private boolean handleNavigation(Uri uri) {
        String scheme = uri.getScheme() == null ? "" : uri.getScheme().toLowerCase();
        String host = uri.getHost() == null ? "" : uri.getHost().toLowerCase();
        if (("https".equals(scheme) || "http".equals(scheme)) && APP_HOST.equals(host)) {
            return false;
        }
        try {
            startActivity(new Intent(Intent.ACTION_VIEW, uri));
        } catch (ActivityNotFoundException error) {
            Toast.makeText(this, "Não foi possível abrir este endereço.", Toast.LENGTH_SHORT).show();
        }
        return true;
    }

    private View createSplashView() {
        LinearLayout panel = centeredPanel();
        ImageView logo = new ImageView(this);
        logo.setImageResource(R.drawable.apex_icon);
        logo.setContentDescription("Apex Combate");
        logo.setScaleType(ImageView.ScaleType.CENTER_CROP);
        panel.addView(logo, size(176, 176));

        TextView title = text("APEX COMBATE", 24, TEXT, true);
        LinearLayout.LayoutParams titleParams = wrapContent();
        titleParams.topMargin = dp(18);
        panel.addView(title, titleParams);

        TextView subtitle = text("Uma plataforma. Todas as lutas.", 14, MUTED, false);
        LinearLayout.LayoutParams subtitleParams = wrapContent();
        subtitleParams.topMargin = dp(7);
        panel.addView(subtitle, subtitleParams);

        ProgressBar progress = new ProgressBar(this);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            progress.setIndeterminateTintList(ColorStateList.valueOf(ACCENT));
        }
        LinearLayout.LayoutParams progressParams = size(42, 42);
        progressParams.topMargin = dp(28);
        panel.addView(progress, progressParams);

        FrameLayout container = overlayContainer();
        container.addView(panel, centeredWrap());
        return container;
    }

    private View createOfflineView() {
        LinearLayout panel = centeredPanel();
        panel.setPadding(dp(28), dp(28), dp(28), dp(28));
        panel.setBackgroundColor(SURFACE);

        ImageView logo = new ImageView(this);
        logo.setImageResource(R.drawable.apex_icon);
        logo.setContentDescription("Apex Combate");
        logo.setScaleType(ImageView.ScaleType.CENTER_CROP);
        panel.addView(logo, size(112, 112));

        TextView title = text("Sem conexão com o Apex", 21, TEXT, true);
        LinearLayout.LayoutParams titleParams = wrapContent();
        titleParams.topMargin = dp(18);
        panel.addView(title, titleParams);

        TextView message = text("Conecte-se à internet para carregar a demonstração oficial.", 14, MUTED, false);
        message.setGravity(Gravity.CENTER);
        LinearLayout.LayoutParams messageParams = wrapContent();
        messageParams.topMargin = dp(9);
        panel.addView(message, messageParams);

        Button retry = new Button(this);
        retry.setText("TENTAR NOVAMENTE");
        retry.setTextColor(Color.WHITE);
        retry.setTextSize(13);
        retry.setAllCaps(false);
        retry.setBackgroundColor(ACCENT);
        retry.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                offlineView.setVisibility(View.GONE);
                splashView.setVisibility(View.VISIBLE);
                webView.loadUrl(APP_URL);
            }
        });
        LinearLayout.LayoutParams retryParams = new LinearLayout.LayoutParams(dp(220), dp(52));
        retryParams.topMargin = dp(24);
        panel.addView(retry, retryParams);

        FrameLayout container = overlayContainer();
        FrameLayout.LayoutParams panelParams = new FrameLayout.LayoutParams(
                Math.min(dp(420), getResources().getDisplayMetrics().widthPixels - dp(36)),
                ViewGroup.LayoutParams.WRAP_CONTENT,
                Gravity.CENTER);
        container.addView(panel, panelParams);
        return container;
    }

    private void showOffline() {
        mainFrameFailed = true;
        splashView.setVisibility(View.GONE);
        offlineView.setVisibility(View.VISIBLE);
    }

    private FrameLayout overlayContainer() {
        FrameLayout container = new FrameLayout(this);
        container.setBackgroundColor(BACKGROUND);
        return container;
    }

    private LinearLayout centeredPanel() {
        LinearLayout panel = new LinearLayout(this);
        panel.setOrientation(LinearLayout.VERTICAL);
        panel.setGravity(Gravity.CENTER_HORIZONTAL);
        return panel;
    }

    private TextView text(String value, int sizeSp, int color, boolean bold) {
        TextView text = new TextView(this);
        text.setText(value);
        text.setTextSize(sizeSp);
        text.setTextColor(color);
        text.setGravity(Gravity.CENTER);
        if (bold) text.setTypeface(text.getTypeface(), android.graphics.Typeface.BOLD);
        return text;
    }

    private FrameLayout.LayoutParams matchParent() {
        return new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT);
    }

    private FrameLayout.LayoutParams centeredWrap() {
        return new FrameLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.CENTER);
    }

    private LinearLayout.LayoutParams wrapContent() {
        return new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
    }

    private LinearLayout.LayoutParams size(int widthDp, int heightDp) {
        return new LinearLayout.LayoutParams(dp(widthDp), dp(heightDp));
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == FILE_CHOOSER_REQUEST && fileChooserCallback != null) {
            Uri[] result = WebChromeClient.FileChooserParams.parseResult(resultCode, data);
            fileChooserCallback.onReceiveValue(result);
            fileChooserCallback = null;
        }
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        webView.saveState(outState);
        super.onSaveInstanceState(outState);
    }

    @Override
    protected void onPause() {
        webView.onPause();
        super.onPause();
    }

    @Override
    protected void onResume() {
        super.onResume();
        webView.onResume();
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) webView.goBack();
        else super.onBackPressed();
    }

    @Override
    protected void onDestroy() {
        if (fileChooserCallback != null) {
            fileChooserCallback.onReceiveValue(null);
            fileChooserCallback = null;
        }
        webView.stopLoading();
        webView.setWebChromeClient(null);
        webView.setWebViewClient(null);
        webView.destroy();
        super.onDestroy();
    }
}
