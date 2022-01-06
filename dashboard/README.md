# Applied Data Science Capstone Dashboard

This dashboard was build using the Dash framework and deployed on Google Cloud Platform.

You can review the [live application here](https://ibm-course-capstone.uc.r.appspot.com).

The first interactive component is a **Dropdown** list, where you can select all sites or any specific launch site to plot the graphs for.​

A **Pie Chart** is shown according to the selected option. Each slice on this graph represents the total of **successful launches** per site or the success / failure ratio.​

Then a **Scatter Plot** is displayed, where the **launch outcome** in relation to the **payload mass** can be analyzed. Each point on this graph is colored according to the booster version label on the right side.​

Finally, you can switch the **RangeSlider** on top of the Scatter Plot to analyze the results for different payload mass values.