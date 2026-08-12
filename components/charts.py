"""
=========================================================
OmniMind AI Assistant
Chart Components
=========================================================

Reusable Plotly charts for the Streamlit application.

Supports:
- Line charts
- Bar charts
- Pie charts
- Area charts
- Scatter charts
- Histograms
- Box plots
- Heatmaps
- Radar charts
- Gauge charts

Also provides compatibility methods used by
AnalyticsPage:
- line_chart()
- bar_chart()
- pie_chart()
"""

from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


class ChartComponent:
    """
    Collection of reusable Plotly charts.
    """

    # =====================================================
    # BASIC LINE CHART
    # =====================================================

    @staticmethod
    def line(
        data: pd.DataFrame,
        x: str,
        y: str,
        title: str = "",
    ) -> None:

        if data is None or data.empty:
            st.info("No data available for this chart.")
            return

        fig = px.line(
            data,
            x=x,
            y=y,
            title=title,
            markers=True,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # =====================================================
    # BASIC BAR CHART
    # =====================================================

    @staticmethod
    def bar(
        data: pd.DataFrame,
        x: str,
        y: str,
        title: str = "",
    ) -> None:

        if data is None or data.empty:
            st.info("No data available for this chart.")
            return

        fig = px.bar(
            data,
            x=x,
            y=y,
            title=title,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # =====================================================
    # BASIC AREA CHART
    # =====================================================

    @staticmethod
    def area(
        data: pd.DataFrame,
        x: str,
        y: str,
        title: str = "",
    ) -> None:

        if data is None or data.empty:
            st.info("No data available for this chart.")
            return

        fig = px.area(
            data,
            x=x,
            y=y,
            title=title,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # =====================================================
    # BASIC PIE CHART
    # =====================================================

    @staticmethod
    def pie(
        data: pd.DataFrame,
        names: str,
        values: str,
        title: str = "",
    ) -> None:

        if data is None or data.empty:
            st.info("No data available for this chart.")
            return

        fig = px.pie(
            data,
            names=names,
            values=values,
            title=title,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # =====================================================
    # ANALYTICS LINE CHART
    # =====================================================

    @staticmethod
    def line_chart(
        data: Any,
    ) -> None:
        """
        Compatibility method used by AnalyticsPage.

        Expected input:

        [
            {
                "timestamp": "...",
                "requests": 1
            }
        ]

        or a pandas DataFrame.
        """

        if data is None:
            st.info("No usage data available.")
            return

        if isinstance(data, pd.DataFrame):

            df = data.copy()

        else:

            try:
                df = pd.DataFrame(data)

            except Exception:
                st.info("No usage data available.")
                return

        if df.empty:
            st.info("No usage data available.")
            return

        # -------------------------------------------------
        # Find timestamp column
        # -------------------------------------------------

        if "timestamp" not in df.columns:

            df["timestamp"] = range(
                1,
                len(df) + 1,
            )

        # -------------------------------------------------
        # Find numeric column
        # -------------------------------------------------

        numeric_columns = [
            column for column in df.columns if pd.api.types.is_numeric_dtype(df[column])
        ]

        if not numeric_columns:

            st.info("No numeric usage data available.")
            return

        y_column = "requests" if "requests" in df.columns else numeric_columns[0]

        fig = px.line(
            df,
            x="timestamp",
            y=y_column,
            title="Usage Trends",
            markers=True,
        )

        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Requests",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # =====================================================
    # ANALYTICS BAR CHART
    # =====================================================

    @staticmethod
    def bar_chart(
        data: Any,
    ) -> None:
        """
        Compatibility method used by AnalyticsPage.

        Expected input:

        {
            "VisionAgent": 10,
            "ResearchAgent": 5
        }
        """

        if not data:
            st.info("No agent usage data available.")
            return

        # -------------------------------------------------
        # Dictionary input
        # -------------------------------------------------

        if isinstance(data, dict):

            df = pd.DataFrame(
                {
                    "agent": list(data.keys()),
                    "usage": list(data.values()),
                }
            )

        # -------------------------------------------------
        # DataFrame input
        # -------------------------------------------------

        elif isinstance(data, pd.DataFrame):

            df = data.copy()

        # -------------------------------------------------
        # List input
        # -------------------------------------------------

        else:

            try:
                df = pd.DataFrame(data)

            except Exception:
                st.info("No agent usage data available.")
                return

        if df.empty:
            st.info("No agent usage data available.")
            return

        # -------------------------------------------------
        # Detect columns
        # -------------------------------------------------

        if "agent" in df.columns:

            x_column = "agent"

        elif "name" in df.columns:

            x_column = "name"

        else:

            x_column = df.columns[0]

        numeric_columns = [
            column for column in df.columns if pd.api.types.is_numeric_dtype(df[column])
        ]

        if not numeric_columns:

            st.info("No numeric agent usage data available.")
            return

        y_column = "usage" if "usage" in df.columns else numeric_columns[0]

        fig = px.bar(
            df,
            x=x_column,
            y=y_column,
            title="Agent Usage",
        )

        fig.update_layout(
            xaxis_title="Agent",
            yaxis_title="Usage",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # =====================================================
    # ANALYTICS PIE CHART
    # =====================================================

    @staticmethod
    def pie_chart(
        data: Any,
    ) -> None:
        """
        Compatibility method used by AnalyticsPage.

        Expected input:

        {
            "gemini-model": 20,
            "other-model": 5
        }
        """

        if not data:
            st.info("No model distribution data available.")
            return

        # -------------------------------------------------
        # Dictionary input
        # -------------------------------------------------

        if isinstance(data, dict):

            df = pd.DataFrame(
                {
                    "model": list(data.keys()),
                    "usage": list(data.values()),
                }
            )

        # -------------------------------------------------
        # DataFrame input
        # -------------------------------------------------

        elif isinstance(data, pd.DataFrame):

            df = data.copy()

        # -------------------------------------------------
        # List input
        # -------------------------------------------------

        else:

            try:
                df = pd.DataFrame(data)

            except Exception:
                st.info("No model distribution data available.")
                return

        if df.empty:
            st.info("No model distribution data available.")
            return

        # -------------------------------------------------
        # Detect columns
        # -------------------------------------------------

        if "model" in df.columns:

            names_column = "model"

        elif "name" in df.columns:

            names_column = "name"

        else:

            names_column = df.columns[0]

        numeric_columns = [
            column for column in df.columns if pd.api.types.is_numeric_dtype(df[column])
        ]

        if not numeric_columns:

            st.info("No numeric model data available.")
            return

        values_column = "usage" if "usage" in df.columns else numeric_columns[0]

        fig = px.pie(
            df,
            names=names_column,
            values=values_column,
            title="Model Distribution",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # =====================================================
    # SCATTER
    # =====================================================

    @staticmethod
    def scatter(
        data: pd.DataFrame,
        x: str,
        y: str,
        color: str | None = None,
        title: str = "",
    ) -> None:

        if data is None or data.empty:
            st.info("No data available for this chart.")
            return

        fig = px.scatter(
            data,
            x=x,
            y=y,
            color=color,
            title=title,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # =====================================================
    # HISTOGRAM
    # =====================================================

    @staticmethod
    def histogram(
        data: pd.DataFrame,
        column: str,
        title: str = "",
    ) -> None:

        if data is None or data.empty:
            st.info("No data available for this chart.")
            return

        fig = px.histogram(
            data,
            x=column,
            title=title,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # =====================================================
    # BOX
    # =====================================================

    @staticmethod
    def box(
        data: pd.DataFrame,
        x: str,
        y: str,
        title: str = "",
    ) -> None:

        if data is None or data.empty:
            st.info("No data available for this chart.")
            return

        fig = px.box(
            data,
            x=x,
            y=y,
            title=title,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # =====================================================
    # HEATMAP
    # =====================================================

    @staticmethod
    def heatmap(
        matrix: Any,
        title: str = "",
    ) -> None:

        if matrix is None:
            st.info("No heatmap data available.")
            return

        fig = go.Figure(data=go.Heatmap(z=matrix))

        fig.update_layout(title=title)

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # =====================================================
    # RADAR
    # =====================================================

    @staticmethod
    def radar(
        categories: list[str],
        values: list[float],
        title: str = "",
    ) -> None:

        if not categories or not values:
            st.info("No radar data available.")
            return

        fig = go.Figure()

        fig.add_trace(
            go.Scatterpolar(
                r=values,
                theta=categories,
                fill="toself",
                name=title,
            )
        )

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                )
            ),
            title=title,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # =====================================================
    # GAUGE
    # =====================================================

    @staticmethod
    def gauge(
        value: float,
        title: str,
        maximum: float = 100,
    ) -> None:

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=value,
                title={"text": title},
                gauge={
                    "axis": {
                        "range": [
                            0,
                            maximum,
                        ]
                    }
                },
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

charts = ChartComponent()
